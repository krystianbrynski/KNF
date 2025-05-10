import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def connect(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )

    try:
        with engine.begin() as conn:
            create_label_list = '''
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'label_list')
                BEGIN
                    CREATE TABLE label_list (
                        id_label INT PRIMARY KEY,
                        label_tresc NVARCHAR(MAX)
                    )
                END
            '''
            create_data = '''
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'data')
                BEGIN
                    CREATE TABLE data (
                        id_data INT PRIMARY KEY,
                        id_label INT FOREIGN KEY REFERENCES label_list(id_label),
                        data NVARCHAR(MAX),
                        data_point NVARCHAR(100),
                        data_type NVARCHAR(100)
                    )
                END
            '''
            conn.execute(text(create_label_list))
            conn.execute(text(create_data))

            id_label_counter = 1
            id_data_counter = 1

            for label_tresc, content in json_data.items():
                insert_label = '''
                    INSERT INTO label_list (id_label, label_tresc)
                    VALUES (:id_label, :label_tresc)
                '''
                conn.execute(text(insert_label), {
                    "id_label": id_label_counter,
                    "label_tresc": label_tresc
                })

                data_point_list = content.get("data_point", [])
                data_type = content.get("datatype", None)

                for dp in data_point_list:
                    insert_data = '''
                        INSERT INTO data (id_data, id_label, data, data_point, data_type)
                        VALUES (:id_data, :id_label, :data, :data_point, :data_type)
                    '''
                    conn.execute(text(insert_data), {
                        "id_data": id_data_counter,
                        "id_label": id_label_counter,
                        "data": None,
                        "data_point": dp,
                        "data_type": data_type
                    })
                    id_data_counter += 1

                id_label_counter += 1

            print("Data are loaded.")

    except SQLAlchemyError as e:
        print(f"Error {e}")
