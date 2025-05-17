def transform_labels_unique(input_dict,column_flag):
    output = {}
    if column_flag:
        for key, values in input_dict.items():
            label_row = values[0]                      # np. "Liczba zdarzen"
            data_point = values[1]                     # np. ["A", "B"]
            label_col = values[2]
            datatype = values[3] if values[3] else "string"
            qname = values[4]
            output[key] = {
                "rows": label_row,
                "data_point": data_point,
                "cols": label_col,
                "datatype": datatype,
                "qname": qname
            }
    else:
        for key, values in input_dict.items():
            label_row = values[0]                      # np. "Liczba zdarzen"
            data_point = values[1]                     # np. ["A", "B"]
            datatype = values[2]
            qname = values[3]
            output[key] = {
                "rows": label_row,
                "data_point": data_point,
                "datatype": datatype,
                "qname": qname
            }

    return output