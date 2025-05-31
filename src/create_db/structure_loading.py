from typing import List, Optional, Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from pathlib import Path
import json


def create_tables() -> Engine:
    """
    Funkcja używana jest do stworzenia połączenia z bazą danych MSSQL i wymaganych tabel, jeśli nie istnieją.
    Zwraca obiekt SQLAlchemy Engine.
    """
    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    with engine.begin() as conn:
        conn.execute(text('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Taxonomy')
            BEGIN
                CREATE TABLE Taxonomy (
                    id_taxonomy INT PRIMARY KEY IDENTITY(1,1),
                    version NVARCHAR(255),
                    name NVARCHAR(255)
                )
            END
        '''))
        conn.execute(text('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Forms')
            BEGIN
                CREATE TABLE Forms (
                    id_form INT PRIMARY KEY IDENTITY(1,1),
                    name_form NVARCHAR(255) UNIQUE,
                    id_taxonomy INT FOREIGN KEY REFERENCES Taxonomy(id_taxonomy)
                )
            END
        '''))
        conn.execute(text('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Labels')
            BEGIN
                CREATE TABLE Labels (
                    id_label INT PRIMARY KEY IDENTITY(1,1),
                    row_name NVARCHAR(MAX),
                    column_name NVARCHAR(255),       
                    report_name NVARCHAR(255),
                    id_form INT FOREIGN KEY REFERENCES Forms(id_form)
                )
            END
        '''))
        conn.execute(text('''
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
        '''))
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reports')
            BEGIN
                CREATE TABLE Reports (
                    id_report INT PRIMARY KEY IDENTITY(1,1)
                )
            END
        """))
        conn.execute(text("""
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
        """))
    return engine


def load_json_structure(folder_path: str) -> List[Dict[str, Any]]:
    """
     Wczytuje wszystkie pliki JSON z podanego folderu i zwraca listę ich zawartości.
     Pliki zawierają wcześniej wygenerowaną strukturę taksonomii.
     """
    folder = Path(folder_path).resolve()
    json_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == '.json']

    if not json_files:
        return []

    all_jsons = []
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_jsons.append(data)

    return all_jsons


def load_taxonomy_version_from_file(json_path: str) -> tuple[str | None, str | None]:
    """
        Funkcja jest stosowana w procesie sprawdzania wersji taksonomii.
       Wczytuje plik JSON zawierający informację na temat wersji i nazwy ładowanej taksonomii
        i zwraca te informacje.
       """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("version"), data.get("name")


def check_and_insert_taxonomy_version(engine, taxonomy_json_path: str) -> int | None:
    """
    Funkcja używana jest do rozpoznania czy ładowana struktura danych nie została już wcześniej załadowana do MSSQL.
    Proces polega na sprawdzeniu czy wersja i nazwa taksonomii już istnieje w bazie danych.
    Jeśli nie, dodaje ją i zwraca `id_taxonomy`. Jeśli istnieje – zwraca None.
    """
    version, name = load_taxonomy_version_from_file(taxonomy_json_path)

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT id_taxonomy FROM Taxonomy WHERE version = :version"),
            {"version": version}
        ).first()

        if existing:
            print(f"Struktura z wersją {version} już istnieje – pomijam ładowanie struktury.")
            return None

        result = conn.execute(
            text("INSERT INTO Taxonomy (version, name) OUTPUT INSERTED.id_taxonomy VALUES (:version, :name)"),
            {"version": version, "name": name}
        )
        id_taxonomy = result.scalar_one()
        print(f"Dodano nową wersję taxonomy: {version} z id {id_taxonomy}")
        return id_taxonomy


def create_structure(folder_path: str, folder_path_2: str):
    """
    Główna funkcja odpowiedzialna za:
    - tworzenie tabel w bazie,
    - sprawdzenie i ewentualne wstawienie nowej wersji taksonomii,
    - zapis całej struktury danych z wcześniej wygenerowanych plików JSON
    Zwraca obiekt Engine dla bazy danych.
    """
    engine = create_tables() # tworzenie tabel
    id_taxonomy = check_and_insert_taxonomy_version(engine, folder_path_2) # sprawdza czy nowa wersja taksonomii jest już w bazie, jeśli nie, to ją dodaje

    if id_taxonomy is None:
        return engine

    all_jsons = load_json_structure(folder_path)

    try:
        with engine.begin() as conn:
            # Pobieramy wszystkie już istniejące formularze z bazy:
            existing_forms = conn.execute(
                text("SELECT id_form, name_form FROM Forms")
            ).mappings().all()
            existing_forms_dict = {row['name_form']: row['id_form'] for row in existing_forms}

            for json_obj in all_jsons:
                form_name = json_obj.get("form_name")
                form_data = json_obj.get("data", {})

                if form_name in existing_forms_dict:
                    id_form = existing_forms_dict[form_name]
                else:
                    result = conn.execute(
                        text("INSERT INTO Forms (name_form, id_taxonomy) OUTPUT INSERTED.id_form VALUES (:name_form, :id_taxonomy)"),
                        {"name_form": form_name, "id_taxonomy": id_taxonomy}
                    )
                    id_form = result.scalar_one()
                    existing_forms_dict[form_name] = id_form

                for label_key, label_content in form_data.items():
                    row_value = label_content.get("value_row")

                    cols = label_content.get("value_columns", [])
                    if isinstance(cols, str):
                        cols = [] if cols.lower().strip() in ("none", "") else [cols]
                    elif cols is None or not isinstance(cols, list):
                        cols = []

                    data_points = label_content.get("data_points", [])
                    if not isinstance(data_points, list):
                        data_points = []
                    data_type = label_content.get("datatype")
                    report_name = label_content.get("sheet_name")
                    qname = label_content.get("qname")

                    row_value = row_value or None
                    report_name = report_name or None
                    data_type = data_type or None
                    qname = qname or None

                    max_len = max(len(cols), len(data_points))
                    cols += [None] * (max_len - len(cols))
                    data_points += [None] * (max_len - len(data_points))

                    for col_value, data_point in zip(cols, data_points):
                        col_value = col_value or None
                        data_point = data_point or None

                        result = conn.execute(
                            text('''
                                INSERT INTO Labels (row_name, column_name, report_name, id_form)
                                OUTPUT INSERTED.id_label
                                VALUES (:row_name, :column_name, :report_name, :id_form)
                            '''), {
                                "row_name": row_value,
                                "column_name": col_value,
                                "report_name": report_name,
                                "id_form": id_form
                            }
                        )
                        id_label = result.scalar_one()

                        conn.execute(
                            text('''
                                INSERT INTO Data_points (id_label, data_point, qname, data_type)
                                VALUES (:id_label, :data_point, :qname, :data_type)
                            '''), {
                                "id_label": id_label,
                                "data_point": data_point,
                                "qname": qname,
                                "data_type": data_type
                            }
                        )
        print("Data from reports are loaded successfully")

    except SQLAlchemyError as e:
        print({e})


