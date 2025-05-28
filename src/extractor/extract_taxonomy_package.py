import json
from xml.etree.ElementTree import Element
from src.config.constants import TAXONOMY_INFO_PATH

# Funkcja wyciąga z parsowanego pliku XML nazwę oraz wersję taksonomii i zapisuje je do pliku JSON.
# Dane te są potrzebne, aby wprowadzić nazwę oraz wersję taksonomii do tabeli TAXONOMY w bazie danych MSSQL.
# Funkcja została dodana, aby zautomatyzować pobieranie i aktualizację tych informacji,
def collect_name_and_version_taxonomy(tax_parsed: Element)-> None:
    for child in tax_parsed:
        if child.tag.endswith('name'):
            name = child.text
        elif child.tag.endswith('version'):
            version = child.text

    taxonomy_info = {
        "name": name,
        "version": version
    }

    with open(TAXONOMY_INFO_PATH, 'w', encoding='utf-8') as f:
        json.dump(taxonomy_info, f, ensure_ascii=False, indent=2)