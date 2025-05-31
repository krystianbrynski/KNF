from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import json

def load_reports(folder_path: str) -> None:
    """
       Wczytuje pliki JSON zawierający wcześniej wyekstraktowanych danych raportowych i wstawia ich dane do bazy danych.

       Proces:
       - Ładuje wszystkie pliki JSON z folderu.
       - Tworzy nowy wpis w tabeli Reports, aby oznaczyć nowy raport.
       - Pobiera mapowanie dostępnych punktów danych (Datapoints)
       - Iteruje przez każdy plik JSON i zapisuje wartości do tabeli Data,
         łącząc je z nowym raportem i odpowiednimi punktami danych. """

    folder = Path(folder_path)
    all_jsons = []

    for json_file in folder.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_jsons.append(data)

    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    try:
        with engine.begin() as conn:
            # Dodawanie nowego raportu i pobieranie jego ID
            result = conn.execute(text("""
                INSERT INTO Reports OUTPUT INSERTED.id_report DEFAULT VALUES
            """))
            new_id_report = result.scalar_one()

            # Pobieranie mapy: nazwa punktu danych -> id_data_point
            dp_rows = conn.execute(text("SELECT id_data_point, data_point FROM Data_points")).mappings().all()
            data_point_map = {row["data_point"]: row["id_data_point"] for row in dp_rows}

            # Wstawianie danych do bazy danych
            for json_obj in all_jsons:
                for form_name, records in json_obj.items():
                    if not isinstance(records, list):
                        continue
                    for record in records:
                        if not isinstance(record, dict):
                            continue
                        for data_point, value in record.items():
                            id_dp = data_point_map.get(data_point)
                            if id_dp:
                                conn.execute(text("""
                                    INSERT INTO Data (id_report, id_data_point, form_name, data)
                                    VALUES (:id_report, :id_data_point, :form_name, :data)
                                """), {
                                    "id_report": new_id_report,
                                    "id_data_point": id_dp,
                                    "form_name": form_name,
                                    "data": value
                                })
                            else:
                                print(f"[WARNING] Id_datapoint not found: {data_point}")

        print(f"Data from'{folder_path}' was loaded. Id_report={new_id_report}.")

    except SQLAlchemyError as e:
        print({e})
