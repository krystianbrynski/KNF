def transform_labels_unique(input_dict,column_flag,name_report):
    output = {}
    if column_flag:
        for key, values in input_dict.items():
            label_row = values[0]
            data_point = values[1]
            label_col = values[2]
            datatype = values[3] if values[3] else "string"
            qname = values[4]
            output[key] = {
                "row": label_row,
                "data_point": data_point,
                "cols": label_col,
                "datatype": datatype,
                "qname": qname,
                "report_name_sheet": name_report
            }
    else:
        for key, values in input_dict.items():
            label_row = values[0]
            data_point = values[1]
            datatype = values[2]
            qname = values[3]
            label_col = "Null"
            output[key] = {
                "row": label_row,
                "data_point": data_point,
                "cols": label_col,
                "datatype": datatype,
                "qname": qname,
                "report_name_sheet": name_report
            }

    return output