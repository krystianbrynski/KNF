def prepare_data_to_load(rend_labels, lab_codes_labels_and_value, lab_pl_labels_and_value):
    axis_x_labels_data_point = []
    axis_y_labels_data_point = []
    dict_axis_x_labels_data_point = {}
    dict_label_value_data_point = {}
    if 'x' in rend_labels and 'y' in rend_labels:
        idx_x = rend_labels.index('x') if 'x' in rend_labels else None
        idx_y = rend_labels.index('y') if 'y' in rend_labels else None

        if idx_x < idx_y:
            axis_x_labels = rend_labels[:idx_x]
            axis_y_labels = rend_labels[idx_x + 1:idx_y]
        else:
            axis_y_labels = rend_labels[:idx_y]
            axis_x_labels = rend_labels[idx_y + 1:idx_x]

        if len(axis_y_labels) == 0 or len(axis_x_labels) == 0:
            axis_x_labels = rend_labels[:-2]
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

            return dict_label_value_data_point, False

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
            label_x = []
            for j in axis_x_labels_data_point:
                data_points.append(i[1] + "X" + j[1])
                label_x.append(j[0])
            dict_axis_x_labels_data_point[i[0]] = data_points

        label_x_and_value = []
        for i in label_x:
            for j in lab_pl_labels_and_value:
                if i == j[0]:
                    label_x_and_value.append(j[1])
        for i in dict_axis_x_labels_data_point:
            for j in lab_pl_labels_and_value:
                if i == j[0]:
                    dict_label_value_data_point[i] = [j[1], dict_axis_x_labels_data_point[i], label_x_and_value]
        return dict_label_value_data_point, True

    else:  # jeśli tabela ma jedną oś
        axis_x_labels = rend_labels[:-1]
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

    return dict_label_value_data_point, False


def prepare_label_and_data_type(rend_labels_and_qnames, data_types):
    label_and_data_types = []

    for j in rend_labels_and_qnames:
        for i in data_types:
            if i[0] in j[1]:
                label_and_data_types.append([j[0], i[1], i[0]])
                break
    return label_and_data_types


def prepare_type_into_dict(type_list, label_dict):
    for key, type_val, name in type_list:
        if key in label_dict:
            label_dict[key].append(type_val)
            label_dict[key].append(name)

    for i in label_dict:  # jesli nie znajdzie typu danych to string i none
        if len(label_dict[i]) == 3:
            label_dict[i].append('string')
            label_dict[i].append('none')
    return label_dict
