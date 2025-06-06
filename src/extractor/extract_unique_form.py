import os
from typing import List, Set


def extract_form_name(dirname: str) -> str:
    """Funkcja dzieli nazwę folderu na segmenty rozdzielone kropkami i zwraca pierwsze trzy segmenty połączone ponownie
    kropkami. Jest to używane do wyodrębnienia nazwy arkusza z pełnej nazwy folderu, np. z "n.pif.bk.00" uzyskamy
    "n.pif.bk."""

    parts = dirname.split(".")
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return dirname


def collect_unique_form_names(tab_path: str) -> List[str]:
    """Funkcja, która wyciąga unikalne nazwy formularzy na podstawie nazw folderów znajdujących się w katalogu 'tab'.
       Jest potrzebna do zidentyfikowania, ile unikalnych formularzy znajduje się w taksonomii.
       Na podstawie nazw folderów można określić, które formularze należy przetworzyć,
       co stanowi punkt wyjścia do dalszego przetwarzania danych i budowy finalnej struktury."""

    unique_form_names: Set[str] = set()

    for dirname in os.listdir(tab_path):
        full_path = os.path.join(tab_path, dirname)
        if os.path.isdir(full_path):
            form_name = extract_form_name(dirname)
            unique_form_names.add(form_name)

    return sorted(unique_form_names)
