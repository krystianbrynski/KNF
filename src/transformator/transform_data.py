# Funkcja przekształca dane wejściowe (słownik) w zunifikowaną strukturę.
# Dodaje informacje o wierszu, kolumnie (jeśli dotyczy), punkcie danych, typie danych, qname oraz nazwie arkusza.
# Umożliwia obsługę zarówno jedno-, jak i dwuwymiarowych arkuszy (kolumny obecne lub nie).
def transform_data(input_dict, column_flag, sheet_name):
    transformed_data = {}
    for key, values in input_dict.items():
        if column_flag:  # Sprawdzenie warunkowe czy arkusz jest dwuwymiarowy
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

    return transformed_data
