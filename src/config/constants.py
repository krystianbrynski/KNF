
FILE_PATH = r"C:\Users\marta\PycharmProjects\KNF\data\json"


# Ścieżka do pliku XSD z definicjami typów danych
MET_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/dict/met/met.xsd'

# Ścieżka do folderu 'tab', w którym znajdują się podfoldery dla poszczególnych arkuszy.
# W każdym z podfolderów znajdują się pliki opisujące definicje i strukturę odpowiednich arkuszy danych.
TAB_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/fws/bion/bion-2024-12/2024-10-21/tab'

# Ścieżka do pliku zawierającego nazwę i wersję taksonomii
TAXONOMY_PACKAGE_PATH = "../data/taxonomy/TaksonomiaBION/META-INF/taxonomyPackage.xml"

# Ścieżka do pliku, w którym zostanie zapisany JSON z nazwą oraz wersją taksonomii
TAXONOMY_INFO_PATH = "../structure/taxonomy_info/taxonomy_info.json"

# Nazwy kluczowe plików do wyszukiwania w ścieżkach
LAB_PL = 'lab-pl'
REND = 'rend'
LAB_CODES = 'lab-codes'

# Domyślne wartości używane, gdy nie uda się dopasować innego typu lub qname
DATA_TYPE = "xbrli:stringItemType"  # Domyślny typ danych (standardowy typ, gdy brak dopasowania)
QNAME = "None"                      # Domyślny qname, jeśli nie uda się dopasować


