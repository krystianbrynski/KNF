from src.config.constants import DATA_TYPE, QNAME

# Funkcja, która łączy dane wyciągnięte z plików rend, lab-pl oraz lab-codes dla jednowymiarowego arkusza.
def combine_data_axis_y(lab_codes_labels_and_value, lab_pl_labels_and_value, axis_y_labels):
    axis_y_labels_data_points = []
    dict_label_value_data_point = {}
    dict_label_data_point = {}

    for y_label in axis_y_labels:
        for label, value in lab_codes_labels_and_value:
            if y_label == label and int(value) % 10 == 0:
                axis_y_labels_data_points.append((label, value))

    for y_label, y_data_point in axis_y_labels_data_points:
        dict_label_data_point[y_label] = [y_data_point]

    for y_label in dict_label_data_point:
        for label, value in lab_pl_labels_and_value:
            if y_label == label:
                dict_label_value_data_point[y_label] = [value, dict_label_data_point[y_label]]

    return dict_label_value_data_point, False  # Zwraca słownik oraz informację, czy arkusz jest dwuwymiarowy — w tym przypadku False (arkusz jednowymiarowy)

# Funkcja, która łączy dane wyciągnięte z plików rend, lab-pl oraz lab-codes dla dwuwymiarowego arkusza.
def combine_data_axis_x_and_y(lab_codes_labels_and_value, lab_pl_labels_and_value,axis_x_labels, axis_y_labels):
    axis_x_labels_data_points = []
    axis_y_labels_data_points = []
    axis_x_values = []
    combined_x_points_by_y_label = {}
    dict_label_value_data_point = {}

    for x_label in axis_x_labels:
        for code_label, code_value in lab_codes_labels_and_value:
            if x_label == code_label and int(code_value) % 10 == 0:
                axis_x_labels_data_points.append((code_label, code_value))

    for y_label in axis_y_labels:
        for code_label, code_value in lab_codes_labels_and_value:
            if y_label == code_label and int(code_value) % 10 == 0:
                axis_y_labels_data_points.append((code_label, code_value))

    for y_label, y_data_point in axis_y_labels_data_points:
        data_points = []
        label_x = []
        for x_label, x_data_point in axis_x_labels_data_points:
            data_points.append(y_data_point + "X" + x_data_point)
            label_x.append(x_label)
        combined_x_points_by_y_label[y_label] = data_points

    for x_label in label_x:
        for label, value in lab_pl_labels_and_value:
            if x_label == label:
                axis_x_values.append(value)

    for y_label in combined_x_points_by_y_label:
        for label, value in lab_pl_labels_and_value:
            if y_label == label:
                dict_label_value_data_point[y_label] = [value, combined_x_points_by_y_label[y_label], axis_x_values]

    return dict_label_value_data_point, True # Zwraca słownik oraz informację, czy arkusz jest dwuwymiarowy — w tym przypadku True (arkusz dwuwymiarowy)

# Funkcja zwraca słownik, w którym:
# - kluczami są etykiety (label) z osi Y (np. 'uknf_c34'),
# - wartościami są listy zawierające:
#   - etykietę tekstową przypisaną do labela Y (np. 'Imię'),
#   - etykietę tekstową przypisaną do labela X, jeśli arkusz jest dwuwymiarowy,
#   - listę punktów danych (tzw. data points),
#     np. ['0010'] dla formularza jednowymiarowego lub ['0010X0020'] dla dwuwymiarowego
def combine_data_from_files(rend_labels, lab_codes_labels_and_value, lab_pl_labels_and_value):
    if 'x' in rend_labels and 'y' in rend_labels:# Sprawdzenie, czy w danych z pliku REND występują obie osie: "x" i "y" (oznacza formularz dwuwymiarowy)
        idx_x = rend_labels.index('x')
        idx_y = rend_labels.index('y')

        # W pliku REND osie "x" i "y" mogą występować w różnej kolejności (np. [uknf_c1, uknf_c2, x, uknf_c3, y] lub [uknf_c1, uknf_c2, y, uknf_c3, x]).
        # Dlatego ten warunek sprawdza, która oś pojawia się wcześniej, aby poprawnie podzielić etykiety na osie X i Y.
        if idx_x < idx_y:
            axis_y_labels = rend_labels[idx_x + 1:idx_y]
            axis_x_labels = rend_labels[:idx_x]

        else:
            axis_y_labels = rend_labels[:idx_y]
            axis_x_labels = rend_labels[idx_y + 1:idx_x]

        # Mimo że warunek wykrył formularz jako dwuwymiarowy, może wystąpić sytuacja, w której do osi X nie jest przypisany żaden label.
        # W takim przypadku traktujemy formularz jako jednowymiarowy.
        # Przykład takiej sytuacji: [uknf_c1, uknf_c2, y, x], gdzie wszystkie etykiety przypisane są do osi Y, a oś X zawiera np. tylko wymiar techniczny.
        if len(axis_y_labels) == 0 or len(axis_x_labels) == 0:
            axis_y_labels = rend_labels[:-2]
            return combine_data_axis_y(lab_codes_labels_and_value, lab_pl_labels_and_value, axis_y_labels)

        else:
            return combine_data_axis_x_and_y(lab_codes_labels_and_value, lab_pl_labels_and_value,axis_x_labels,axis_y_labels)

    else:  # Jeśli arkusz jest jednowymiarowy
        axis_y_labels = rend_labels[:-1]
        return combine_data_axis_y(lab_codes_labels_and_value, lab_pl_labels_and_value, axis_y_labels)


# Funkcja zwraca listę trójek [label, data_type, name],
def match_labels_with_data_types(rend_labels_and_qnames, data_types):
    label_and_data_types = []

    for label, qname in rend_labels_and_qnames:
        for name, data_type in data_types:
            if name in qname:
                label_and_data_types.append([label, data_type, name])
                break

    return label_and_data_types


def match_datatypes_and_qnames(labels_and_data_types, combine_data):
    for key, type_val, name in labels_and_data_types:  # Dodanie typów danych oraz nazw metryk do słownika, jeśli jest możliwość dopasowania
        if key in combine_data:
            combine_data[key].append(type_val)
            combine_data[key].append(name)

    for key in combine_data:  # jesli nie znajdzie typu danych to dodajemy ustandaryzowany typ danej oraz nazwy metryki, który można znaleźć w configu

        # Weryfikacja struktury danych w combine_data, czy brakuje typu danych i nazwy metryki:
        # - Jeśli długość listy to 2, oznacza to dane jednowymiarowe,
        #   czyli lista zawiera tylko: [wartość_wiersza, [punkty_danych]].
        # - Jeśli długość listy to 3, oznacza dane dwuwymiarowe,
        #   czyli lista zawiera: [wartość_wiersza, [punkty_danych], [wartości_kolumn]].
        #
        # W przypadku długości 2 lub 3 brakuje jeszcze informacji o typie danych i nazwie metryki,
        # więc dopisujemy ustandaryzowany typ danych (DATA_TYPE) oraz nazwę metryki (QNAME), który jest zainicjalizowany w configu.
        if len(combine_data[key]) == 3 or len(combine_data[key]) == 2:
            combine_data[key].append(DATA_TYPE)
            combine_data[key].append(QNAME)

    return combine_data
