import sqlite3
import json

example_file_path = "C:/Users/marta/PycharmProjects/KNF/create_db/przyklad.json"


with open(example_file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

#
conn = sqlite3.connect("KNF.db")
cursor = conn.cursor()


for table_name, columns in json_data.items():
    if columns:
        try:

            kolumny_sql = ", ".join([f'"{column}" TEXT' for column in columns])

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    {kolumny_sql}
                )
            ''')
            print(f"Tabela '{table_name}' została utworzona lub już istnieje.")


            pusty_rekord = tuple([None] * len(columns))
            cursor.execute(
                f'INSERT INTO "{table_name}" ({", ".join([f"\"{column}\"" for column in columns])}) '
                f'VALUES ({", ".join(["?" for _ in columns])})',
                pusty_rekord
            )
            print(f"Rekord wstawiony do tabeli '{table_name}'.")

        except Exception as e:
            print(f"Błąd przy przetwarzaniu tabeli '{table_name}': {e}")

conn.commit()
conn.close()
