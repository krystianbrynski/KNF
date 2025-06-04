import os
from typing import List, Tuple

from src.config.constants import TAB_PATH
from src.config.constants import LAB_PL
from src.config.constants import REND
from src.config.constants import LAB_CODES


def collect_target_paths_and_sheet_name(form_names: List[str]) -> List[Tuple[List[str], str]]:
    """Funkcja została stworzona po to, aby dla każdego folderu docelowego (np. 'n.pif.bk.00')
       zebrać listę ścieżek do plików zawierających w nazwie frazy:
       'rend', 'lab-pl' lub 'lab-codes'.
       Celem działania funkcji jest zebranie wszystkich istotnych plików źródłowych
       powiązanych z danym arkuszem, tak aby możliwe było dalsze przetwarzanie danych
       z tych plików i wykorzystanie ich do zbudowania finalnej, kompletnej struktury danych."""

    target_paths_and_sheet_name: List[Tuple[List[str], str]] = []

    for form_name in form_names:  # Iteracja po unikalnych nazwach formularzy
        for item_name in os.listdir(TAB_PATH):
            path_full = os.path.join(TAB_PATH, item_name)

            if os.path.isdir(path_full) and item_name.startswith(
                    form_name):  # Sprawdzenie, czy to folder i czy jego nazwa zaczyna się od nazwy formularza
                target_paths = []
                for file_name in os.listdir(path_full):
                    file_name_clean = file_name.strip()
                    file_path = os.path.join(path_full, file_name_clean)

                    if os.path.isfile(file_path):  # Sprawdzenie, czy to plik i czy zawiera interesujące słowa kluczowe
                        if LAB_PL in file_name or REND in file_name or LAB_CODES in file_name:
                            target_paths.append(file_path)

                sheet_name = item_name
                target_paths_and_sheet_name.append((target_paths, sheet_name))

    return target_paths_and_sheet_name
