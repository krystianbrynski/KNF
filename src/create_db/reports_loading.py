import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from src.config.constants import INSERT_INTO_DATA_TABLE, INSERT_INTO_REPORTS_TABLE, REPORTS_JSON_PATH, \
    SELECT_DATAPOINTS_TABLE


def load_folder_reports() -> Optional[List[Dict[str, Any]]]:
    folder = Path(REPORTS_JSON_PATH)
    all_jsons: List[Dict[str, Any]] = []

    for json_file in folder.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_jsons.append(data)

    if len(all_jsons) == 0:
        return None

    return all_jsons


def validate_structure(all_jsons: List[Dict[str, Any]], conn: Connection) -> bool:
    for json_obj in all_jsons:
        for form_name, records in json_obj.items():
            id_datapoint_and_datapoint = conn.execute(text(SELECT_DATAPOINTS_TABLE),
                                                      {"form_name": form_name}).mappings().all()
            data_points_report: list[str] = []
            data_points_structure: list[str] = []

            for record in records:
                for data_point in record:
                    data_points_report.append(data_point)

            for datapoint_record in id_datapoint_and_datapoint:
                data_points_structure.append(datapoint_record["data_point"])

            if not all(elem in data_points_structure for elem in data_points_report):
                return False
    return True


def load_data(conn: Connection, all_jsons: List[Dict[str, Any]]) -> None:
    result = conn.execute(text(INSERT_INTO_REPORTS_TABLE))
    id_report = result.scalar_one()

    for json_obj in all_jsons:
        for form_name, records in json_obj.items():
            id_datapoint_and_datapoint = conn.execute(text(SELECT_DATAPOINTS_TABLE),
                                                      {"form_name": form_name}).mappings().all()
            data_point_map = {row["data_point"]: row["id_data_point"] for row in id_datapoint_and_datapoint}

            for record in records:
                for data_point, value in record.items():
                    id_data_point = data_point_map[data_point]
                    conn.execute(text(INSERT_INTO_DATA_TABLE), {
                        "id_report": id_report,
                        "id_data_point": id_data_point,
                        "form_name": form_name,
                        "data": value
                    })

    print("Twoje dane z raportów zostaly załadowane do bazy danych")


def load_report() -> None:
    """
       Wczytuje pliki JSON zawierający wcześniej wyekstraktowanych danych raportowych i wstawia ich dane do bazy danych.

       Proces:
       - Ładuje wszystkie pliki JSON z folderu.
       - Tworzy nowy wpis w tabeli Reports, aby oznaczyć nowy raport.
       - Pobiera mapowanie dostępnych punktów danych (Datapoints)
       - Iteruje przez każdy plik JSON i zapisuje wartości do tabeli Data,
         łącząc je z nowym raportem i odpowiednimi punktami danych. """

    all_jsons = load_folder_reports()

    if all_jsons is None:
        print("Error: Brak wyekstraktowanych jsonow z raportu!")
        return None

    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )

    try:
        with engine.begin() as conn:
            if validate_structure(all_jsons, conn):
                load_data(conn, all_jsons)
            else:
                print("Struktra którą próbujesz załadować jest inna niż w bazie danych, w formularzu występują inne "
                      "datapointy niż w bazie danych")
                return None

    except SQLAlchemyError as e:
        print({e})
