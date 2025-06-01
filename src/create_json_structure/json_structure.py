import json
from dataclasses import asdict

from src.config.constants import MET_PATH
from src.config.constants import TAB_PATH
from src.config.constants import TAXONOMY_PACKAGE_PATH
from src.config.constants import STRUCTURE_PATH

from src.extractor.extract_data_types import extract_types_and_names
from src.extractor.extract_lab_codes_file import extract_lab_codes_labels_and_values
from src.extractor.extract_namespaces import extract_namespaces
from src.extractor.extract_rend_file import extract_rend_labels_and_qnames
from src.extractor.extract_rend_file import extract_rend_ordered_labels_and_axes
from src.extractor.extract_target_paths import collect_target_paths_and_sheet_name
from src.extractor.extract_unique_form import collect_unique_form_names
from src.extractor.extract_lab_pl_file import extract_lab_pl_labels_and_values
from src.extractor.extract_taxonomy_package import collect_name_and_version_taxonomy
from src.merge.merge_data import combine_data_from_files
from src.merge.merge_data import match_datatypes_and_qnames
from src.merge.merge_data import match_labels_with_data_types

from src.parser.xml import parse_xml

from src.transformator.transform_data import transform_data
from typing import List, Tuple


# Funkcja integruje wszystkie moduły niezbędne do wyodrębnienia wszystkich wymaganych danych,
# łączy je w jedną spójną strukturę, a następnie zapisuje tę strukturę do pliku JSON.
# Zapisane pliki JSON służą później jako źródło do załadowania danych do bazy danych MSSQL.
#
# Funkcja została stworzona, aby zautomatyzować i uprościć proces przetwarzania danych,
# zapewniając spójność i ułatwiając późniejszą ich integrację z bazą danych.
def build_json_for_sheet(lab_codes_path: str,
                         rend_path: str,
                         lab_pl_path: str,
                         data_types_with_names: List[Tuple[str, str]],
                         sheet_name: str,
                         form_name: str) -> None:

    lab_codes_parsed = parse_xml(lab_codes_path)
    rend_parsed = parse_xml(rend_path)
    lab_pl_parsed = parse_xml(lab_pl_path)
    lab_pl_namespaces = extract_namespaces(lab_pl_path)
    rend_labels_and_qnames = extract_rend_labels_and_qnames(rend_parsed)
    rend_labels = extract_rend_ordered_labels_and_axes(rend_parsed)
    lab_codes_labels_and_value = extract_lab_codes_labels_and_values(lab_codes_parsed)
    lab_pl_labels_and_value = extract_lab_pl_labels_and_values(lab_pl_parsed, lab_pl_namespaces)
    combine_data, column_flag = combine_data_from_files(rend_labels, lab_codes_labels_and_value, lab_pl_labels_and_value)
    labels_and_data_types = match_labels_with_data_types(rend_labels_and_qnames, data_types_with_names)
    data_with_types = match_datatypes_and_qnames(labels_and_data_types, combine_data)
    final_data = transform_data(data_with_types, column_flag, sheet_name,form_name)

    with open(f'{STRUCTURE_PATH}/{sheet_name}.json', 'a', encoding='utf-8') as json_file:
        json.dump(asdict(final_data), json_file, ensure_ascii=False, indent=4)


# Główna funkcja odpowiedzialna za tworzenie struktury w bazie danych.
# Dla każdego arkusza wywołuje funkcję build_json_for_sheet, która generuje
# odpowiednią strukturę zapisaną w formacie JSON.
def create_structure() -> None:
    met_parsed = parse_xml(MET_PATH)
    form_names = collect_unique_form_names(TAB_PATH)
    data_types_with_names = extract_types_and_names(met_parsed)
    target_paths_and_sheet_name = collect_target_paths_and_sheet_name(form_names)
    tax_parsed = parse_xml(TAXONOMY_PACKAGE_PATH)
    collect_name_and_version_taxonomy(tax_parsed)

    for form_name in form_names:
        for (lab_codes_path, lab_pl_path, rend_path), sheet_name in target_paths_and_sheet_name:
            if form_name in lab_codes_path and form_name in lab_pl_path and form_name in rend_path:  # Sprawdzenie, czy nazwa arkusza występuje w nazwach wszystkich trzech ścieżek
                build_json_for_sheet(lab_codes_path, rend_path, lab_pl_path, data_types_with_names, sheet_name,
                                     form_name)
