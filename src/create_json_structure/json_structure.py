import json

from src.config.constants import MET_PATH
from src.config.constants import TAB_PATH

from src.extractor.extract_data_types import extract_types_and_names
from src.extractor.extract_lab_codes_file import extract_lab_codes_labels_and_values
from src.extractor.extract_namespaces import extract_namespaces
from src.extractor.extract_rend_file import extract_rend_labels_and_qnames
from src.extractor.extract_rend_file import extract_rend_ordered_labels_and_axes
from src.extractor.extract_target_paths import collect_target_paths_and_sheet_name
from src.extractor.extract_unique_form import collect_unique_form_names
from src.extractor.extract_lab_pl_file import extract_lab_pl_labels_and_values

from src.merge.merge_data import combine_data_from_files
from src.merge.merge_data import match_datatypes_and_qnames
from src.merge.merge_data import match_labels_with_data_types

from src.parser.xml import parse_xml

from src.transformator.transform_data import transform_data


# Funkcja tworzy strukture w pliku json dla jednego arkusza
def build_json_for_sheet(lab_codes_path,rend_path,lab_pl_path,data_types_with_names,sheet_name,form_name):
    lab_codes_parsed = parse_xml(lab_codes_path)
    rend_parsed = parse_xml(rend_path)
    lab_pl_parsed = parse_xml(lab_pl_path)
    lab_pl_namespaces = extract_namespaces(lab_pl_path)
    rend_labels_and_qnames = extract_rend_labels_and_qnames(rend_parsed)
    rend_labels = extract_rend_ordered_labels_and_axes(rend_parsed)
    lab_codes_labels_and_value = extract_lab_codes_labels_and_values(lab_codes_parsed)
    lab_pl_labels_and_value = extract_lab_pl_labels_and_values(lab_pl_parsed, lab_pl_namespaces)
    combine_data, column_flag = combine_data_from_files(rend_labels, lab_codes_labels_and_value,lab_pl_labels_and_value)
    labels_and_data_types = match_labels_with_data_types(rend_labels_and_qnames, data_types_with_names)
    data_with_types = match_datatypes_and_qnames(labels_and_data_types, combine_data)
    transformed_data = transform_data(data_with_types, column_flag, sheet_name)
    wrapped_data = {f"{form_name}": transformed_data}

    with open(f'../data/json/{sheet_name}.json', 'a', encoding='utf-8') as json_file:
        json.dump(wrapped_data, json_file, ensure_ascii=False, indent=4)


# Funkcja, która dla każdego formularza:
# - wyszukuje odpowiadające mu pliki źródłowe (rend, lab-pl, lab-codes),
# - wywołuje funkcję create_json_file, która tworzy strukturę danych i zapisuje ją do pliku JSON,
# - proces ten jest powtarzany dla wszystkich arkuszy.
def create_structure() -> None:
    met_parsed = parse_xml(MET_PATH)
    form_names = collect_unique_form_names(TAB_PATH)
    data_types_with_names = extract_types_and_names(met_parsed)
    target_paths_and_sheet_name = collect_target_paths_and_sheet_name(form_names)

    for form_name in form_names:
        for (lab_codes_path, lab_pl_path, rend_path), sheet_name in target_paths_and_sheet_name:
            if form_name in lab_codes_path and form_name in lab_pl_path and form_name in rend_path:  # Sprawdzenie, czy nazwa arkusza występuje w nazwach wszystkich trzech ścieżek
               build_json_for_sheet(lab_codes_path,rend_path,lab_pl_path,data_types_with_names,sheet_name,form_name)