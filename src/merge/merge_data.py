from typing import List, Tuple, Dict, Union
from src.config.data_classes import OneDimensionalAxis, TwoDimensionalAxis

# Funkcja, która łączy dane wyciągnięte z plików rend, lab-pl oraz lab-codes dla jednowymiarowego arkusza.

def combine_one_dimensional_data(lab_codes_labels_and_value: List[Tuple[str, str]]
                        , lab_pl_labels_and_value: List[Tuple[str, str]],
                        axis_labels: list[str],
                        axis: str) -> Tuple[Dict[str, OneDimensionalAxis], bool]:

    axis_labels_data_points: List[Tuple[str, str]] = []
    dict_label_value_data_point: Dict[str, 'OneDimensionalAxis'] = {}
    dict_label_data_point: Dict[str, List[str]] = {}

    for axis_label in axis_labels:
        for label, value in lab_codes_labels_and_value:
            if axis_label == label and int(value) % 10 == 0:
                axis_labels_data_points.append((label, value))

    for axis_label, axis_data_point in axis_labels_data_points:
        dict_label_data_point[axis_label] = [axis_data_point]

    for axis_label in dict_label_data_point:
        for label, text in lab_pl_labels_and_value:
            if axis_label == label:
                dict_label_value_data_point[axis_label] = OneDimensionalAxis(
                        text=text,
                        data_points=dict_label_data_point[axis_label],
                        axis=axis,
                    )

    return dict_label_value_data_point, False  # Zwraca słownik oraz informację, czy arkusz jest dwuwymiarowy — w tym przypadku False (arkusz jednowymiarowy)

# Funkcja, która łączy dane wyciągnięte z plików rend, lab-pl oraz lab-codes dla dwuwymiarowego arkusza.
def combine_two_dimensional_data(lab_codes_labels_and_value: List[Tuple[str, str]],
                              lab_pl_labels_and_value: List[Tuple[str, str]],
                              axis_x_labels: list[str], axis_y_labels: list[str])-> Tuple[Dict[str, TwoDimensionalAxis], bool]:

    axis_x_labels_data_points: List[Tuple[str, str]] = []
    axis_y_labels_data_points: List[Tuple[str, str]] = []
    axis_x_values: List[str] = []
    label_x: list[str] = []
    combined_x_points_by_y_label: Dict[str, List[str]] = {}
    dict_label_value_data_point: Dict[str, TwoDimensionalAxis] = {}

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
        for label, text in lab_pl_labels_and_value:
            if y_label == label:
                dict_label_value_data_point[y_label] =  TwoDimensionalAxis(
                        row_text=text,
                        data_points=combined_x_points_by_y_label[y_label],
                        column_texts=axis_x_values
                    )

    return dict_label_value_data_point, True # Zwraca słownik oraz informację, czy arkusz jest dwuwymiarowy — w tym przypadku True (arkusz dwuwymiarowy)

# Funkcja została stworzona w celu połączenia danych z trzech plików XML: REND, LAB_CODES oraz LAB_PL.
# Każdy z plików dostarcza inne informacje:
# - REND: służy do określenia, które etykiety (labels) przypisane są do osi X i Y.
# - LAB_CODES: przypisanie technicznych etykiet (label) do punktów danych (data points),
# - LAB_PL: przypisanie technicznych etykiet (label) do wartosci tekstowych
#
# Wynik tej funkcji to wstępnie połączona struktura danych w formie słownika,
# która integruje etykiety przypisane do wierszy i kolumn oraz wykonuje ich crossowanie,
# aby uzyskać powiązania między wierszami a kolumnami
#
# Dane będą później przetwarzany w celu dodania typów danych, nazw metryk, nazwy arkusza oraz nazwy formularza w celu uzyskania pełnej struktury danych.
def combine_data_from_files(rend_labels: List[str],
                            lab_codes_labels_and_value: List[Tuple[str, str]],
                            lab_pl_labels_and_value: List[Tuple[str, str]]) -> Tuple[Union[Dict[str, TwoDimensionalAxis], Dict[str, OneDimensionalAxis]], bool]:

    if 'x' in rend_labels and 'y' in rend_labels:# Sprawdzenie, czy w danych z pliku REND występują obie osie: "x" i "y" (oznacza formularz dwuwymiarowy)
        idx_x = rend_labels.index('x')
        idx_y = rend_labels.index('y')

        # W pliku REND osie "x" i "y" mogą występować w różnej kolejności (np. [uknf_c1, uknf_c2, x, uknf_c3, y] lub [uknf_c1, uknf_c2, y, uknf_c3, x]).
        # Dlatego ten warunek sprawdza, która oś pojawia się wcześniej, aby poprawnie podzielić etykiety na osie x i y.
        if idx_x < idx_y:
            axis_y_labels = rend_labels[idx_x + 1:idx_y]
            axis_x_labels = rend_labels[:idx_x]

        else:
            axis_y_labels = rend_labels[:idx_y]
            axis_x_labels = rend_labels[idx_y + 1:idx_x]

        # Mimo że warunek wykrył formularz jako dwuwymiarowy, może wystąpić sytuacja, w której do osi x nie jest przypisany żaden label.
        # W takim przypadku traktujemy formularz jako jednowymiarowy.
        # Przykład takiej sytuacji: [uknf_c1, uknf_c2, y, x], gdzie wszystkie etykiety przypisane są do osi y, a oś x zawiera np. tylko wymiar techniczny (jednak my wyciągamy tylko labele, wiec np. wymiar nie będzie zawarty).
        if len(axis_y_labels) == 0 or len(axis_x_labels) == 0:
            axis_labels = rend_labels[:-2]
            axis = rend_labels[-2]
            return combine_one_dimensional_data(lab_codes_labels_and_value, lab_pl_labels_and_value, axis_labels, axis)

        else:
            return combine_two_dimensional_data(lab_codes_labels_and_value, lab_pl_labels_and_value,axis_x_labels,axis_y_labels)

    else:  # Jeśli arkusz jest jednowymiarowy
        axis_labels = rend_labels[:-1]
        axis = rend_labels[-1]
        return combine_one_dimensional_data(lab_codes_labels_and_value, lab_pl_labels_and_value, axis_labels, axis)


#  Funkcja została stworzona po to, aby dopasować do każdego z podanych labeli odpowiednią metrykę (nazwę) oraz jej typ danych
def match_labels_with_data_types(rend_labels_and_qnames: List[Tuple[str, str]], data_types: List[Tuple[str, str]])-> List[List[str]]:
    label_and_data_types: List[List[str]] = []

    for label, qname in rend_labels_and_qnames:
        for name, data_type in data_types:
            if name in qname:
                label_and_data_types.append([label, data_type, name])
                break

    return label_and_data_types

#Ta funkcja została napisana po to, aby do istniejącej struktury danych (słownika combine_data)
#dopisać informacje o typie danych (data_type) oraz nazwie metryki (qname) dla danego klucza (labela)
def match_datatypes_and_qnames(labels_and_data_types: List[List[str]],
                               combine_data: Union[Dict[str, TwoDimensionalAxis], Dict[str, OneDimensionalAxis]])->Union[Dict[str, TwoDimensionalAxis], Dict[str, OneDimensionalAxis]]:

    for key, type_val, name in labels_and_data_types:  # Dodanie typów danych oraz nazw metryk do słownika, jeśli jest możliwość dopasowania
        if key in combine_data:
            combine_data[key].data_typ = type_val
            combine_data[key].qname = name

    return combine_data
