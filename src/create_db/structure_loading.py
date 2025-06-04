import json

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from typing import Any, Dict, List, Optional

from src.config import constants
from src.config.constants import STRUCTURE_JSON_PATH, TAXONOMY_INF_PATH


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


def load_json_structure() -> Optional[List[Dict[str, Any]]]:
    """
     Wczytuje wszystkie pliki JSON z wcześniej wygenerowaną strukturę taksonomii z podanego folderu i zwraca listę ich
     zawartości.
     """

    folder = Path(STRUCTURE_JSON_PATH).resolve()
    json_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == '.json']

    if not json_files:
        print("Brak utworzonej struktury, brak plików transportowych json")
        return None

    all_jsons: List[Dict[str, Any]] = []
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_jsons.append(data)

    return all_jsons


def load_taxonomy_version_from_file() -> tuple[str, str]:
    """
    Funkcja jest stosowana w procesie sprawdzania wersji taksonomii.
    Wczytuje plik JSON zawierający informację na temat wersji i nazwy ładowanej taksonomii
    i zwraca te informacje.
    """

    with open(TAXONOMY_INF_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("version"), data.get("name")


def check_and_insert_taxonomy_version(engine) -> int | None:
    """
    Funkcja używana jest do rozpoznania czy ładowana struktura danych nie została już wcześniej załadowana do bazy.
    Proces polega na sprawdzeniu czy wersja i nazwa taksonomii już istnieje w bazie danych.
    Jeśli nie, dodaje ją i zwraca `id_taxonomy`. Jeśli istnieje – zwraca None.
    """
    version, name = load_taxonomy_version_from_file()

    with engine.begin() as conn:
        existing = conn.execute(
            text(constants.SELECT_TAXONOMY_TABLE),
            {"version": version}
        ).first()

        if existing:
            print(f"Struktura z wersj {version} już istnieje – pomijam ładowanie struktury.")
            return None

        result = conn.execute(
            text(constants.INSERT_INTO_TAXONOMY_TABLE),
            {"version": version, "name": name}
        )
        id_taxonomy = result.scalar_one()
        print(f"Dodano nową wersję taxonomy: {version}")
        return id_taxonomy


def load_form_name(conn: Connection, form_name: str, id_taxonomy: int) -> int:
    result = conn.execute(
        text(constants.INSERT_INTO_FORMS_TABLE),
        {"name_form": form_name, "id_taxonomy": id_taxonomy}
    )
    id_form = result.scalar_one()

    return id_form


def load_labels_and_datapoints(conn: Connection, id_form: int, label_content: Dict[str, Any]) -> None:
    row_value = label_content.get("value_row")
    col_values = label_content.get("value_columns")
    data_points = label_content.get("data_points")
    data_type = label_content.get("datatype")
    sheet_name = label_content.get("sheet_name")
    qname = label_content.get("qname")

    for col_value, data_point in zip(col_values, data_points):
        result = conn.execute(
            text(constants.INSERT_INTO_LABELS_TABLE), {
                "row_name": row_value,
                "column_name": col_value,
                "sheet_name": sheet_name,
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


def load_taxonomy_structure(engine: Engine, all_jsons: List[Dict[str, str]], id_taxonomy: int) -> None:
    """ Ładuje strukturę taksonomii wywołująć dwie funkcje: """
    form_names: list[str] = []
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

            print("Struktura bazodanowa została utworzona pomyślnie")
    except SQLAlchemyError as e:
        print({e})


def create_structure() -> bool:
    """
    Funkcja tworzy strukturę taksonomii w bazie danych jeśli nie została załadowana do niej wcześniej.
    Używając funkcji 'check_and_insert_taxonomy_version' sprawdza czy nowa wersja i nazwa taksonomii jest już w bazie,
    jeśli nie, to ją dodaje.
    """
    engine = create_tables()
    all_jsons = load_json_structure()

    id_taxonomy = check_and_insert_taxonomy_version(engine)

    if all_jsons is None or id_taxonomy is None:
        return False

    load_taxonomy_structure(engine, all_jsons, id_taxonomy)
    return True
