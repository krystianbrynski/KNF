from typing import List, Optional, Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from pathlib import Path
import json
from src.config import constants


def create_tables() -> Engine:
    """
    Funkcja używana jest do stworzenia połączenia z bazą danych MSSQL i wymaganych tabel, jeśli nie istnieją.
    Zwraca obiekt SQLAlchemy Engine.
    """
    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    with engine.begin() as conn:
        conn.execute(text(constants.CREATE_TABLE_TAXONOMY))
        conn.execute(text(constants.CREATE_TABLE_FORMS))
        conn.execute(text(constants.CREATE_TABLE_LABELS))
        conn.execute(text(constants.CREATE_TABLE_DATAPOINTS))
        conn.execute(text(constants.CREATE_TABLE_REPORTS))
        conn.execute(text(constants.CREATE_TABLE_DATA))
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


def load_taxonomy_version_from_file(json_path: str) -> tuple[str, str]:
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
            text(constants.SELECT_TAXONOMY_TABLE),
            {"version": version}
        ).first()

        if existing:
            print(f"Struktura z wersją {version} już istnieje – pomijam ładowanie struktury.")
            return None

        result = conn.execute(
            text(constants.INSERT_INTO_TAXONOMY_TABLE),
            {"version": version, "name": name}
        )
        id_taxonomy = result.scalar_one()
        print(f"Dodano nową wersję taxonomy: {version} z id {id_taxonomy}")
        return id_taxonomy


def load_form_name(conn, form_name, id_taxonomy):
    result = conn.execute(
        text(constants.INSERT_INTO_FORMS_TABLE),
        {"name_form": form_name, "id_taxonomy": id_taxonomy}
    )
    id_form = result.scalar_one()

    return id_form


def load_labels_and_datapoints(conn, id_form, label_content):
    row_value = label_content.get("value_row")
    col_values = label_content.get("value_columns")
    data_points = label_content.get("data_points")
    data_type = label_content.get("datatype")
    report_name = label_content.get("sheet_name")
    qname = label_content.get("qname")

    for col_value, data_point in zip(col_values, data_points):
        result = conn.execute(
            text(constants.INSERT_INTO_LABELS_TABLE), {
                "row_name": row_value,
                "column_name": col_value,
                "report_name": report_name,
                "id_form": id_form
            }
        )
        id_label = result.scalar_one()
        conn.execute(
            text(constants.INSERT_INTO_DATAPOINTS_TABLE), {
                "id_label": id_label,
                "data_point": data_point,
                "qname": qname,
                "data_type": data_type
            }
        )


def load_structure(engine, all_jsons, id_taxonomy):
    form_names = []
    try:
        with engine.begin() as conn:
            for json_obj in all_jsons:
                form_name = json_obj.get("form_name")
                form_data = json_obj.get("data", {})

                if form_name not in form_names:
                    id_form = load_form_name(conn, form_name, id_taxonomy)
                form_names.append(form_name)

                for label_key, label_content in form_data.items():
                    load_labels_and_datapoints(conn, id_form, label_content)

            print("Data from reports are loaded successfully")
    except SQLAlchemyError as e:
        print({e})


def create_structure(folder_path: str, folder_path_2: str):
    """
    Główna funkcja odpowiedzialna za:
    - tworzenie tabel w bazie,
    - sprawdzenie i ewentualne wstawienie nowej wersji taksonomii,
    - zapis całej struktury danych z wcześniej wygenerowanych plików JSON
    Zwraca obiekt Engine dla bazy danych.
    """
    engine = create_tables()  # tworzenie tabel
    id_taxonomy = check_and_insert_taxonomy_version(engine, folder_path_2)  # sprawdza czy nowa wersja taksonomii jest już w bazie, jeśli nie, to ją dodaje

    if id_taxonomy is None:
        return engine

    all_jsons = load_json_structure(folder_path)
    load_structure(engine, all_jsons, id_taxonomy)
