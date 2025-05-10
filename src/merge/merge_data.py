def prepare_data_to_load(rend_labels, lab_codes_labels_and_value, lab_pl_labels_and_value):
    axis_x_labels_data_point = []
    axis_y_labels_data_point = []
    dict_axis_x_labels_data_point = {}
    dict_label_value_data_point = {}

    if 'uknf_a2.root' in rend_labels:  # jeśli tabela ma dwie osie
        axis_x_labels = rend_labels[1:rend_labels.index('uknf_a2.root')]
        axis_y_labels = rend_labels[rend_labels.index('uknf_a2.root') + 1:]

        for i in axis_x_labels:
            for j in lab_codes_labels_and_value:
                if i == j[0] and int(j[1]) % 10 == 0:
                    axis_x_labels_data_point.append(j)

        for i in axis_y_labels:
            for j in lab_codes_labels_and_value:
                if i == j[0] and int(j[1]) % 10 == 0:
                    axis_y_labels_data_point.append(j)
        for i in axis_y_labels_data_point:
            data_points = []
            for j in axis_x_labels_data_point:
                data_points.append(i[1] + "X" + j[1])
            dict_axis_x_labels_data_point[i[0]] = data_points

    else:  # jeśli tabela ma jedną oś
        axis_x_labels = rend_labels[1:]

        for i in axis_x_labels:
            for j in lab_codes_labels_and_value:
                if i == j[0] and int(j[1]) % 10 == 0:
                    axis_x_labels_data_point.append(j)

        for i in axis_x_labels_data_point:
            dict_axis_x_labels_data_point[i[0]] = [i[1]]

    for i in dict_axis_x_labels_data_point:
        for j in lab_pl_labels_and_value:
            if i == j[0]:
                dict_label_value_data_point[i] = [j[1], dict_axis_x_labels_data_point[i]]

    return dict_label_value_data_point

def prepare_label_and_data_type(rend_labels_and_qnames, data_types):
    label_and_data_types = []

    for j in rend_labels_and_qnames:
        for i in data_types:
            if i[0] in j[1]:
                label_and_data_types.append([j[0], i[1]])
                break
    return label_and_data_types

def prepare_type_into_dict(type_list, label_dict):
    for key, type_val in type_list:
        if key in label_dict:
            label_dict[key].append(type_val)
    return label_dict