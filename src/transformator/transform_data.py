# Funkcja tworzy słownik, którego kluczem głównym jest "label" np."uknf_c1".
# Zawiera on:
# - tekst wiersza,
# - tekst znajdujący się w kolumnach (jeśli występują) lub Null,
# - przecięcia,
# - typ danych,
# - nazwę metryki,
# - nazwę arkusza.
# Funkcja obsługuje zarówno arkusze jednowymiarowe, jak i dwuwymiarowe.
def transform_data(data_with_types, column_flag, sheet_name):
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

    return transformed_data
