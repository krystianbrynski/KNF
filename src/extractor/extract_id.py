import os
import pandas as pd

def extract_report_id():
    FOLDER_PATH = '../data/reports'

    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(FOLDER_PATH, filename)
            break

    df = pd.read_excel(file_path, header=None)
    row_idx = df.apply(lambda row: row.astype(str).str.contains("Identyfikator formularza", case=False).any(), axis=1)
    row_index = df[row_idx].index[0]
    print(f"Identyfikator formularza znajduje się w wierszu: {row_index}")
    reports_id = df.iloc[row_index].dropna().tolist()[1:]
    return reports_id
