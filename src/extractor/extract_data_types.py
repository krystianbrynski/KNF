from typing import List, Tuple
from xml.etree.ElementTree import Element


# Funkcja została stworzona po to, aby zidentyfikować i wyodrębnić wszystkie metryki (name)
# wraz z przypisanymi im typami danych z dokumentu XML.
#
# Dzięki temu można później:
# - przypisywać poprawne typy danych do metryk,
# - dopasowywać je do unikalnych etykiet (labeli) dla danego arkusza,
#   co jest kluczowe przy tworzeniu finalnej, ustandaryzowanej struktury danych.
def extract_types_and_names(met_parsed: Element) -> List[Tuple[str, str]]:
    data_types_with_names: List[Tuple[str, str]] = []

    for elem in met_parsed.iter():
        if elem.tag.endswith('element'):
            name = elem.attrib.get('name')
            typ = elem.attrib.get('type')
            if name and typ:
                data_types_with_names.append((name, typ))

    return data_types_with_names
