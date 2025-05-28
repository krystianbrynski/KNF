import pandas as pd
from typing import List, Tuple
import json
import os

def remove_miara_column(df: pd.DataFrame) -> pd.DataFrame:
    col_with_miara = []
    for col in df.columns:
        if (df[col] == "Miara").any():
            col_with_miara.append(col)
    df_clean = df.drop(columns=col_with_miara)
    return df_clean

def find_sequence_positions(df: pd.DataFrame) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    positions_0010 = [(r, c) for r in range(df.shape[0]) for c in range(df.shape[1])
                      if str(df.iat[r, c]).zfill(4) == "0010"]

    if len(positions_0010) == 2:
        (r1, c1), (r2, c2) = positions_0010
        # Komórka z mniejszym indeksem kolumny to start pionowy
        if c1 < c2:
            vertical_start = (r1, c1)
            horizontal_start = (r2, c2)
        else:
            vertical_start = (r2, c2)
            horizontal_start = (r1, c1)

    elif len(positions_0010) == 1:
        r, c = positions_0010[0]

        def safe_int(val_str: str) -> int:
            try:
                return int(val_str)
            except ValueError:
                return -1

        # Sprawdź pionowo
        has_vertical = False
        for nr in range(r + 1, df.shape[0]):
            cell_val = str(df.iat[nr, c]).zfill(4)
            val_int = safe_int(cell_val)
            if val_int == 20 or val_int == 30 or (cell_val.startswith("00") and val_int > 10):
                has_vertical = True
                break

        # Sprawdź poziomo
        has_horizontal = False
        for nc in range(c + 1, df.shape[1]):
            cell_val = str(df.iat[r, nc]).zfill(4)
            val_int = safe_int(cell_val)
            if val_int == 20 or val_int == 30 or (cell_val.startswith("00") and val_int > 10):
                has_horizontal = True
                break

        if has_vertical and not has_horizontal:
            vertical_start = (r, c)
            horizontal_start = None
        elif has_horizontal and not has_vertical:
            horizontal_start = (r, c)
            vertical_start = None
        else:
            raise ValueError("Brak kontynuacji sekwencji po '0010' w arkuszu.")

    else:
        raise ValueError(f"Niepoprawna liczba komórek '0010' w arkuszu: {len(positions_0010)}")


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
                cell_val_int = int(str(cell).zfill(4))
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
                cell_val_int = int(str(cell).zfill(4))
            except ValueError:
                break
            if cell_val_int == val:
                vertical_positions.append((row, c))
                val += 10
                row += 1
            else:
                break

    return horizontal_positions, vertical_positions

def extract_intersections(df, positions_horizontal, positions_vertical):
    results = []
    for (row_v, col_v) in positions_vertical:
        for (row_h, col_h) in positions_horizontal:
            val = df.iat[row_v, col_h]
            if pd.notna(val):
                key = f"{df.iat[row_v, col_v]}X{df.iat[row_h, col_h]}"
                results.append({key: val})
    return results

def extract_from_horizontal(df, positions_horizontal):
    results = []

    code_to_col = {df.iat[row, col]: col for (row, col) in positions_horizontal}

    col_0020 = code_to_col.get("0020")
    start_row = positions_horizontal[0][0] + 1
    for row in range(start_row, len(df)):
        if pd.isna(df.iat[row, col_0020]):
            break

        datapoint_result = {}
        for code, col in code_to_col.items():
            val = df.iat[row, col]
            if pd.notna(val):
                datapoint_result[code] = val

        if datapoint_result:
            results.append(datapoint_result)

    return results

def extract_from_vertical(df, positions_vertical):
    results = []
    for (row, col) in positions_vertical:
        datapoint = df.iat[row, col]
        current_col = col + 1
        while current_col < len(df.columns):
            val = df.iat[row, current_col]
            if pd.notna(val):
                results.append({
                    datapoint: val
                })
                break
            current_col += 1
    return results

def get_all_excel_files_recursive(folder_path: str) -> list[str]:
    excel_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                full_path = os.path.join(root, filename)
                excel_files.append(full_path)
    return excel_files

path = r"C:\Users\marta\PycharmProjects\KNF10\data\reports\PiF_BK_c2025_2024_XXX_0.xlsx"
output_dir = r"C:\Users\marta\PycharmProjects\KNF10\data\json_reports"
os.makedirs(output_dir, exist_ok=True)


xls = pd.ExcelFile(path)

print(f" Przetwarzanie pliku: {path}")

for sheet_name in xls.sheet_names[2:]:
    try:
        df = xls.parse(sheet_name, header=None, dtype=str)
        df = remove_miara_column(df)
        positions_horizontal, positions_vertical = find_sequence_positions(df)

        if positions_horizontal and positions_vertical:
            results = extract_intersections(df, positions_horizontal, positions_vertical)
        elif positions_horizontal:
            results = extract_from_horizontal(df, positions_horizontal)
        elif positions_vertical:
            results = extract_from_vertical(df, positions_vertical)
        else:
            results = []

        filename = os.path.splitext(os.path.basename(path))[0]
        json_filename = os.path.join(output_dir, f"{filename}__{sheet_name}.json")
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump({sheet_name: results}, f, ensure_ascii=False, indent=4)

        print(f" Zapisano: {json_filename}")

    except Exception as e:
        print(f"Błąd w arkuszu {sheet_name} z pliku {path}: {e}")