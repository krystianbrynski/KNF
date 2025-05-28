FILE_PATH = r"..\data\json"
REPORTS_PATH = r"..\data\json_reports"


# Ścieżka do pliku XSD z definicjami typów danych
MET_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/dict/met/met.xsd'

# Ścieżka do folderu 'tab', w którym znajdują się podfoldery dla poszczególnych arkuszy.
# W każdym z podfolderów znajdują się pliki opisujące definicje i strukturę odpowiednich arkuszy danych.
TAB_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/fws/bion/bion-2024-12/2024-10-21/tab'

# Nazwy kluczowe plików do wyszukiwania w ścieżkach
LAB_PL = 'lab-pl'
REND = 'rend'
LAB_CODES = 'lab-codes'

# Domyślne wartości używane, gdy nie uda się dopasować innego typu lub qname
DATA_TYPE = "xbrli:stringItemType"  # Domyślny typ danych (standardowy typ, gdy brak dopasowania)
QNAME = "None"                      # Domyślny qname, jeśli nie uda się dopasować

