from pathlib import Path
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def reports(folder_path: str):
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
            #Creating tables if they don't exists
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


            conn.execute(text("INSERT INTO Reports DEFAULT VALUES"))
            result = conn.execute(text("SELECT CAST(SCOPE_IDENTITY() AS INT) AS last_id"))
            new_id_report = result.scalar_one()


            dp_rows = conn.execute(text("SELECT id_data_point, data_point FROM Data_points")).mappings().all()
            data_point_map = {row["data_point"]: row["id_data_point"] for row in dp_rows}

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
                                print(f"[WARNING] Id_datapoint not found {data_point}")

        print(f"Data from folder '{folder_path}' are loaded. Id_report={new_id_report}.")

    except SQLAlchemyError as e:
        print( {e})