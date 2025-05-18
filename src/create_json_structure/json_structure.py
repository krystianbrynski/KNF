import json
import os
from pathlib import Path

from src.parser.xml import parse_xml
from src.extractor.lab_codes import extract_lab_codes_file
from src.extractor.rend import extract_rend_file
from src.extractor.rend import extract_rend_file_labels_and_qnames
from src.extractor.lab_pl import extract_lab_pl_file
from src.extractor.namespaces import extract_namespaces
from src.extractor.data_types import extract_types
from src.merge.merge_data import prepare_data_to_load
from src.merge.merge_data import prepare_label_and_data_type
from src.merge.merge_data import prepare_type_into_dict
from src.transformator.transform_data import transform_labels_unique

def extract_prefix(name: str) -> str:
    parts = name.split(".")
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return name

def collect_unique_folder_prefixes(root_dir: str):
    unique_names = set()

    for dirpath, dirnames,_  in os.walk(root_dir):
        for dirname in dirnames:
            prefix = extract_prefix(dirname)
            unique_names.add(prefix)

    return sorted(unique_names)

def create_json_structure() -> None:
    met = parse_xml(r'..\data\taxonomy\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\dict\met\met.xsd')
    folder_path = "../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/fws/bion/bion-2024-12/2024-10-21/tab"
    prefixes = collect_unique_folder_prefixes(folder_path)

    for i, prefix in enumerate(prefixes):
        for folder_name in os.listdir(folder_path):
            folder_path_full = os.path.join(folder_path, folder_name)

            if os.path.isdir(folder_path_full) and folder_name.startswith(prefix):
                files_of_interest = []

                for file_name in os.listdir(folder_path_full):
                    file_name_clean = file_name.strip()
                    file_path = os.path.join(folder_path_full, file_name_clean)

                    if os.path.isfile(file_path):
                        if 'lab-pl' in file_name or 'rend' in file_name or 'lab-codes' in file_name:
                            files_of_interest.append(file_path)

                lab_codes_parsed = parse_xml(files_of_interest[0])
                rend_parsed = parse_xml(files_of_interest[2])
                lab_pl_parsed = parse_xml(files_of_interest[1])
                lab_pl_namespaces = extract_namespaces(files_of_interest[1])
                data_types = extract_types(met)
                rend_labels_and_qnames = extract_rend_file_labels_and_qnames(rend_parsed)
                rend_labels = extract_rend_file(rend_parsed)
                lab_codes_labels_and_value = extract_lab_codes_file(lab_codes_parsed)
                lab_pl_labels_and_value = extract_lab_pl_file(lab_pl_parsed, lab_pl_namespaces)

                data, column_flag = prepare_data_to_load(rend_labels, lab_codes_labels_and_value,
                                                                 lab_pl_labels_and_value)

                label_and_data_type = prepare_label_and_data_type(rend_labels_and_qnames, data_types)
                data_with_types = prepare_type_into_dict(label_and_data_type, data)
                transformed_data = transform_labels_unique(data_with_types, column_flag, folder_name)
                folder_name = Path(files_of_interest[0]).parent.name

                wrapped_data = {f"{prefix}": transformed_data}

                with open(f'../data/json/{folder_name}.json', 'a', encoding='utf-8') as json_file:
                   json.dump(wrapped_data, json_file, ensure_ascii=False, indent=4)