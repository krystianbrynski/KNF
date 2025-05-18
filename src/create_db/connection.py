import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path


def load_all_json_from_folder(folder_path: str):
    folder = Path(folder_path)
    all_jsons = []

    for json_file in folder.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_jsons.append(data)
    return all_jsons


def connect(folder_path):
    all_jsons = load_all_json_from_folder(folder_path)
    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )

    try:
        with engine.begin() as conn:

            create_forms_table = '''
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Forms')
                BEGIN
                    CREATE TABLE Forms (
                        id_form INT PRIMARY KEY IDENTITY(1,1),
                        name_form NVARCHAR(255) UNIQUE
                    )
                END
            '''
            create_labels_table = '''
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
            '''
            create_data_points_table = '''
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
            conn.execute(text(create_forms_table))
            conn.execute(text(create_labels_table))
            conn.execute(text(create_data_points_table))


            existing_forms = conn.execute(
                text("SELECT id_form, name_form FROM Forms")
            ).mappings().all()
            existing_forms_dict = {row['name_form']: row['id_form'] for row in existing_forms}

            for json_obj in all_jsons:
                for form_name, form_content in json_obj.items():

                    if form_name in existing_forms_dict:
                        id_form = existing_forms_dict[form_name]
                    else:
                        result = conn.execute(
                            text("INSERT INTO Forms (name_form) OUTPUT INSERTED.id_form VALUES (:name_form)"),
                            {"name_form": form_name}
                        )
                        id_form = result.scalar_one()
                        existing_forms_dict[form_name] = id_form

                    for label_key, label_content in form_content.items():
                        row_value = label_content.get("rows")
                        cols = label_content.get("cols", [])
                        data_points = label_content.get("data_point", [])
                        data_type = label_content.get("datatype")
                        report_name = label_content.get("report_name")
                        qname = label_content.get("qname")


                        for col_value, data_point in zip(cols, data_points):

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
            print("Data are loaded.")

    except SQLAlchemyError as e:
        print(f"Error: {e}")
