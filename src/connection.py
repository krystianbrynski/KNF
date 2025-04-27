import pyodbc
import json

example_file_path = "C:/Users/marta/PycharmProjects/KNF/src/przyklad.json"

with open(example_file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'
                      r'SERVER=localhost\SQLEXPRESS;'
                      r'DATABASE=KNF;'
                      r'Trusted_Connection=yes')
cursor = conn.cursor()


for table_name, columns in json_data.items():
    if columns:
        try:
            kolumny_sql = ", ".join([f'[{column}] NVARCHAR(MAX)' for column in columns])

            cursor.execute(f'''
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{table_name}')
                BEGIN
                    CREATE TABLE [{table_name}] (
                        {kolumny_sql}
                    )
                END
            ''')
            print(f"{table_name} is created.")

            null = tuple([None] * len(columns))

            cursor.execute(
                f'INSERT INTO [{table_name}] ({", ".join([f"[{column}]" for column in columns])}) '
                f'VALUES ({", ".join(["?" for _ in columns])})',
                null
            )
            print(f"Insert:'{table_name}'.")

        except Exception as e:
            print(f"Error in '{table_name}': {e}")


conn.commit()
conn.close()
