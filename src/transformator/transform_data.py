# Funkcja przygotowuje finalną strukturę danych, która może zostać zapisana do pliku JSON.
def transform_data(data_with_types, column_flag: bool, sheet_name: str,form_name: str):
    transformed_data = {}
    for key, values in data_with_types.items():
        if column_flag:   # Obsługa jeśli arkusz jest dwuwymiarowy
            label_row = values[0]
            data_point = values[1]
            label_col = values[2]
            datatype = values[3]
            qname = values[4]

        else:  # Obsługa jeśli arkusz jest jednowymiarowy
            label_row = values[0]
            data_point = values[1]
            label_col = "Null"
            datatype = values[2]
            qname = values[3]

        transformed_data[key] = {
            "value_row": label_row,
            "data_points": data_point,
            "value_columns": label_col,
            "datatype": datatype,
            "qname": qname,
            "sheet_name": sheet_name
        }
    final_data = {f"{form_name}": transformed_data}

    return final_data
