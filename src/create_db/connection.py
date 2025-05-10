import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def connect(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    engine = create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/KNF?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )

    with engine.begin() as conn:
        for table_name, columns in json_data.items():
            if columns:
                try:
                    kolumny_sql = ", ".join([f'[{column}] NVARCHAR(MAX)' for column in columns])

                    create_stmt = f'''
                        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{table_name}')
                        BEGIN
                            CREATE TABLE [{table_name}] (
                                {kolumny_sql}
                            )
                        END
                    '''
                    conn.execute(text(create_stmt))
                    print(f"{table_name} is created.")

                    null_row = {col: None for col in columns}
                    insert_stmt = f'''
                        INSERT INTO [{table_name}] ({", ".join(f"[{col}]" for col in columns)})
                        VALUES ({", ".join(f":{col}" for col in columns)})
                    '''
                    conn.execute(text(insert_stmt), null_row)

                except SQLAlchemyError as e:
                    print(f"Error in '{table_name}': {e}")
