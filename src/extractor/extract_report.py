from src.config.constants import REPORTS_JSON_PATH
from src.config.constants import REPORT_DIR_PATH
from src.config.constants import DROP_LIST
from typing import List, Tuple, Dict, Any, NoReturn
from collections import defaultdict
import pandas as pd
import json
import os


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usuwa kolumny zawierające słowa kluczowe podane w pliku config.

        W arkuszach Excel mogą znajdować się dodatkowe kolumny opisowe, które utrudniają dalszą implementację procesu ekstrakcji.
        Wartości te pojawia się jako etykieta w różnych miejscach tabeli.
        Usunięcie tych kolumn pozwala na poprawne przetwarzanie danych w dalszych krokach."""

    col_to_remove = [
        col for col in df.columns
        if any((df[col] == value).any() for value in DROP_LIST)
    ]

    return df.drop(columns=col_to_remove)


def find_sequence_positions(df: pd.DataFrame) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Znajduje pozycje wartości '0010' w arkuszu i określa położenie sekwencji kodów referencyjncyh - Datapoint'ów.

        W arkuszu wartości zaczynające się od Datapoint'u '0010' wskazują kluczowe punkty początkowe dla sekwencji.
        Funkcja identyfikuje ich położenie, następnie określa położenie kolejnych Datapoint'ów i zapisuje je.
        W późniejszym etapie ekstrakcji Datapoint'y te stanowią punkt odniesienia w ektrakcji danych finansowych."""

    positions_0010 = [
        (r, c) for r in range(df.shape[0]) for c in range(df.shape[1])
        if str(df.iat[r, c]) == "0010"
    ]

    if len(positions_0010) == 2:  # Znalezione dwie wartości '0010' oznaczają obecność dwóch osi Datapoint'ów
        (r1, c1), (r2, c2) = positions_0010

        if c1 < c2:
            vertical_start = (r1, c1)
            horizontal_start = (r2, c2)
        else:
            vertical_start = (r2, c2)
            horizontal_start = (r1, c1)

    elif len(positions_0010) == 1:  ##Znaleziona jedna wartości '0010' oznacza obecność jednej osi
        r, c = positions_0010[0]

        has_vertical = False

        for nr in range(r + 1, df.shape[0]):
            cell_val = str(df.iat[nr, c])

            if cell_val == '0020':
                has_vertical = True
                break

        has_horizontal = False

        for nc in range(c + 1, df.shape[1]):
            cell_val = str(df.iat[r, nc])

            if cell_val == '0020':
                has_horizontal = True
                break

        if has_vertical and not has_horizontal:
            vertical_start = (r, c)
            horizontal_start = None
        elif has_horizontal and not has_vertical:
            horizontal_start = (r, c)
            vertical_start = None
        else:
            raise ValueError("Error determining direction.")

    else:
        raise ValueError(f"Incorrect cell number '0010' in the sheet: {len(positions_0010)}.")

    horizontal_positions = []

    if horizontal_start:
        r, c = horizontal_start
        val = 10
        col = c

        while col < df.shape[1]:
            cell = df.iat[r, col]

            if pd.isna(cell):
                col += 1
                continue

            try:
                cell_val_int = int(str(cell))
            except ValueError:
                break

            if cell_val_int == val:
                horizontal_positions.append((r, col))
                val += 10
                col += 1
            else:
                break

    vertical_positions = []

    if vertical_start:
        r, c = vertical_start
        val = 10
        row = r

        while row < df.shape[0]:
            cell = df.iat[row, c]

            if pd.isna(cell):
                row += 1
                continue

            try:
                cell_val_int = int(str(cell))
            except ValueError:
                break

            if cell_val_int == val:
                vertical_positions.append((row, c))
                val += 10
                row += 1
            else:
                break

    return horizontal_positions, vertical_positions


def extract_intersections(df: pd.DataFrame,
                          positions_horizontal: List[Tuple[int, int]],
                          positions_vertical: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
    """ Funkcja jest wykorzystywana tylko w przypadku jeśli w arkuszu znajdują się sekwencje Datapoint'ów zarówno pionowe jak i poziome.
            Ekstraktuje dane finansowe znajdujące się na miejscu przecięć wcześniej zidentyfikowanych Datapointów."""
    results = []

    for (row_v, col_v) in positions_vertical:
        for (row_h, col_h) in positions_horizontal:
            val = df.iat[row_v, col_h]

            if pd.notna(val):
                key = f"{df.iat[row_v, col_v]}X{df.iat[row_h, col_h]}"
                results.append({key: val})

    return results


def extract_from_horizontal(df: pd.DataFrame, positions_horizontal: List[Tuple[int, int]]) -> List[Dict[str, str]]:
    """ Funkcja jest wykorzystywana do ekstrakcji danych w przypadku jeśli w arkuszu znajdują się sekwencje Datapoint'ów wyłącznie poziome.
            Ekstraktuje dane finansowe bezpośrednio pod wcześniej zidentyfikowanymi Datapointam'i.
             ponieważ w taki sposób rozmieszone są one w arkuszu."""

    results = []

    code_to_col = {df.iat[row, col]: col for (row, col) in positions_horizontal}

    col_0020 = code_to_col.get("0020")
    if col_0020 is None:
        return []

    start_row = positions_horizontal[0][0] + 1

    for row in range(start_row, len(df)):
        if pd.isna(df.iat[row, col_0020]):
            break

        datapoint_result = {}
        for code, col in code_to_col.items():
            if col == 0:  #  pomijamy kolumne z labelem 0010, ponieważ nie mamy jak dodać danych z taksonomi i bez tego struktura będzie nie zgodna
                continue

            val = df.iat[row, col]
            if pd.notna(val):
                datapoint_result[code] = val

        if datapoint_result:
            results.append(datapoint_result)

    grouped = defaultdict(list)
    for record in results:
        for k, v in record.items():
            grouped[k].append(str(v))

    return [{k: ",".join(v)} for k, v in grouped.items()]




def extract_from_vertical(df: pd.DataFrame, positions_vertical: List[Tuple[int, int]]) -> List[Dict[Any, Any]]:
    """ Funkcja jest wykorzystywana do ekstrakcji danych w przypadku jeśli w arkuszu znajdują się sekwencje Datapoint'ów wyłącznie pionowe.
                Ekstraktuje dane finansowe bezpośrednio z prawej strony wcześniej zidentyfikowanych Datapoint'ów,
                 ponieważ w taki sposób rozmieszone są one w arkuszu."""
    results = []

    for (row, col) in positions_vertical:
        datapoint = df.iat[row, col]
        current_col = col + 1

        while current_col < len(df.columns):
            val = df.iat[row, current_col]

            if pd.notna(val):
                results.append({datapoint: val})
                break

            current_col += 1

    return results

def generate_json_reports() -> NoReturn:
    """ Funkcja generuje pliki JSON z raportu Excel, używając wyżej wymionych funkcji."""
    os.makedirs(REPORTS_JSON_PATH, exist_ok=True)

    excel_files = [f for f in os.listdir(REPORT_DIR_PATH) if f.endswith(('.xls', '.xlsx'))]

    if not excel_files:
        print(f"Nie znaleziono pliku Excel w folderze: {REPORT_DIR_PATH}")
        return None
    excel_file_path = os.path.join(REPORT_DIR_PATH, excel_files[0])

    xls = pd.ExcelFile(excel_file_path)

    for sheet_name in xls.sheet_names[2:]:
        df = xls.parse(sheet_name, header=None, dtype=str)
        df = clean_data(df)

        positions_horizontal, positions_vertical = find_sequence_positions(df)

        if positions_horizontal and positions_vertical:
            results = extract_intersections(df, positions_horizontal, positions_vertical)
        elif positions_horizontal:
            results = extract_from_horizontal(df, positions_horizontal)
        elif positions_vertical:
            results = extract_from_vertical(df, positions_vertical)
        else:
            results = []

        filename = os.path.splitext(os.path.basename(excel_file_path))[0]
        json_filename = os.path.join(REPORTS_JSON_PATH, f"{filename}__{sheet_name}.json")

        with open(json_filename, "w", encoding="utf-8") as f:
                json.dump({sheet_name: results}, f, ensure_ascii=False, indent=4)

    print("Dane zostały wyekstraktowane oraz zapisane do katalogu report_data")


