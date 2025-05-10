def transform_labels_unique(input_dict):
    output = {}
    label_counts = {}

    for key, values in input_dict.items():
        label = values[0].strip()
        code = values[1]
        datatype = values[2] if len(values) > 2 else None

        count = label_counts.get(label, 0) + 1
        label_counts[label] = count

        unique_label = f"{label}_{count}" if count > 1 else label

        output[unique_label] = {
            "data_point": code,
            "datatype": datatype
        }

    return output