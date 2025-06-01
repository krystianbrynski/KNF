import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../report_data"))
STRUCTURE_JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../structure/full_structure"))
TAXONOMY_INF_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../structure/taxonomy_info/taxonomy_info.json"))

DROP_LIST = ['miara']  # lista zawiera nazwy pól, które są używane do usuwania niepotrzebnych kolumn

REPORT_DIR_PATH = r"../../data/reports"

# Ścieżka do pliku XSD z definicjami typów danych
MET_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/dict/met/met.xsd'

# Ścieżka do folderu 'tab', w którym znajdują się podfoldery dla poszczególnych arkuszy.
# W każdym z podfolderów znajdują się pliki opisujące definicje i strukturę odpowiednich arkuszy danych.
TAB_PATH = '../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/fws/bion/bion-2024-12/2024-10-21/tab'

# Ścieżka do pliku zawierającego nazwę i wersję taksonomii
TAXONOMY_PACKAGE_PATH = "../data/taxonomy/TaksonomiaBION/META-INF/taxonomyPackage.xml"

# Ścieżka do pliku, w którym zostanie zapisany JSON z nazwą oraz wersją taksonomii
TAXONOMY_INFO_PATH = "../structure/taxonomy_info/taxonomy_info.json"

# Scieżka do folderu, gdzie będą zapisywane strutury w formacie json dla arkuszy
STRUCTURE_PATH = "../structure/full_structure"

# Nazwy kluczowe plików do wyszukiwania w ścieżkach
LAB_PL = 'lab-pl'
REND = 'rend'
LAB_CODES = 'lab-codes'

# Domyślne wartości używane, gdy nie uda się dopasować innego typu lub qname
DATA_TYPE = "xbrli:stringItemType"  # Domyślny typ danych (standardowy typ, gdy brak dopasowania)
QNAME = "None"  # Domyślny qname, jeśli nie uda się dopasować

# Wartość w przypadku braku textu w kolumnie/wierszu
EMPTY = "None"

ACTION = 1


def set_action(value: int):
    global ACTION
    ACTION = value


def get_action():
    global ACTION
    return ACTION


CREATE_TABLE_TAXONOMY = '''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Taxonomy')
            BEGIN
                CREATE TABLE Taxonomy (
                    id_taxonomy INT PRIMARY KEY IDENTITY(1,1),
                    version NVARCHAR(255),
                    name NVARCHAR(255)
                )
            END
        '''

CREATE_TABLE_FORMS = '''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Forms')
            BEGIN
                CREATE TABLE Forms (
                    id_form INT PRIMARY KEY IDENTITY(1,1),
                    name_form NVARCHAR(255),
                    id_taxonomy INT FOREIGN KEY REFERENCES Taxonomy(id_taxonomy)
                )
            END
        '''

CREATE_TABLE_LABELS = '''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Labels')
            BEGIN
                CREATE TABLE Labels (
                    id_label INT PRIMARY KEY IDENTITY(1,1),
                    row_name NVARCHAR(MAX),
                    column_name NVARCHAR(255),       
                    sheet_name NVARCHAR(255),
                    id_form INT FOREIGN KEY REFERENCES Forms(id_form)
                )
            END
        '''

CREATE_TABLE_DATAPOINTS = '''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Data_points')
            BEGIN
                CREATE TABLE Data_points (
                    id_data_point INT PRIMARY KEY IDENTITY(1,1),
                    id_label INT FOREIGN KEY REFERENCES Labels(id_label),
                    data_point NVARCHAR(255),
                    qname NVARCHAR(255),
                    data_type NVARCHAR(255)
                )
            END
        '''

CREATE_TABLE_REPORTS = """
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reports')
            BEGIN
                CREATE TABLE Reports (
                    id_report INT PRIMARY KEY IDENTITY(1,1),
                    report_date_time DATETIME NOT NULL DEFAULT GETDATE()
                )
            END
        """

CREATE_TABLE_DATA = """
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Data')
            BEGIN
                CREATE TABLE Data (
                    id_data INT PRIMARY KEY IDENTITY(1,1),
                    id_report INT FOREIGN KEY REFERENCES Reports(id_report),
                    id_data_point INT FOREIGN KEY REFERENCES Data_points(id_data_point),
                    form_name NVARCHAR(255),
                    data NVARCHAR(MAX)
                )
            END
        """

INSERT_INTO_LABELS_TABLE = '''
                INSERT INTO Labels (row_name, column_name, sheet_name, id_form)
                OUTPUT INSERTED.id_label
                VALUES (:row_name, :column_name, :sheet_name, :id_form)
            '''

INSERT_INTO_DATAPOINTS_TABLE = """INSERT INTO Data_points (id_label, data_point, qname, data_type)
                                            VALUES (:id_label, :data_point, :qname, :data_type)
                                    """

INSERT_INTO_TAXONOMY_TABLE = """INSERT INTO Taxonomy (version, name) OUTPUT INSERTED.id_taxonomy VALUES (:version, :name)"""

INSERT_INTO_FORMS_TABLE = """INSERT INTO Forms (name_form, id_taxonomy) OUTPUT INSERTED.id_form VALUES (:name_form, :id_taxonomy)"""

SELECT_TAXONOMY_TABLE = """SELECT id_taxonomy FROM Taxonomy WHERE version = :version"""

INSERT_INTO_REPORTS_TABLE = """INSERT INTO Reports OUTPUT INSERTED.id_report DEFAULT VALUES
                                """

SELECT_DATAPOINTS_TABLE = """SELECT dp.id_data_point, dp.data_point FROM Data_points dp JOIN Labels l ON dp.id_label = l.id_label WHERE l.sheet_name = :form_name
"""
INSERT_INTO_DATA_TABLE = """INSERT INTO Data (id_report, id_data_point, form_name, data)
                                    VALUES (:id_report, :id_data_point, :form_name, :data)
                                """
