import json

from parser.xml import parse_xml
from find_paths.find_paths import search_paths
from find_paths.find_paths import aim_paths
from extractor.lab_codes import extract_lab_codes_file
from extractor.rend import extract_rend_file
from extractor.rend import extract_rend_file_labels_and_qnames
from extractor.lab_pl import extract_lab_pl_file
from extractor.namespaces import extract_namespaces
from extractor.data_types import extract_types
from extractor.extract_id import extract_report_id
from merge.merge_data import prepare_data_to_load
from merge.merge_data import prepare_label_and_data_type
from merge.merge_data import prepare_type_into_dict
from transformator.transform_data import transform_labels_unique



def run_pipeline() -> None:
    target_folders = extract_report_id()
    paths = search_paths(target_folders)
    lab_pl_rend_lab_codes_paths=  aim_paths(paths)
    met = parse_xml(r'..\data\taxonomy\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\dict\met\met.xsd')
    combined_data = []

    for idx, i in enumerate(lab_pl_rend_lab_codes_paths):
        print(idx)
        lab_codes_parsed = parse_xml(i[0])
        rend_parsed = parse_xml(i[2])
        lab_pl_parsed = parse_xml(i[1])

        lab_pl_namespaces = extract_namespaces(i[1])

        data_types = extract_types(met)
        rend_labels_and_qnames = extract_rend_file_labels_and_qnames(rend_parsed)

        rend_labels = extract_rend_file(rend_parsed)
        lab_codes_labels_and_value = extract_lab_codes_file(lab_codes_parsed)
        lab_pl_labels_and_value = extract_lab_pl_file(lab_pl_parsed,lab_pl_namespaces)

        data = prepare_data_to_load(rend_labels, lab_codes_labels_and_value, lab_pl_labels_and_value)
        label_and_data_type = prepare_label_and_data_type(rend_labels_and_qnames,data_types)

        data_with_types = prepare_type_into_dict(label_and_data_type, data)

        transformed_data = transform_labels_unique(data_with_types)
        combined_data.append(transformed_data)

    with open(f'../data/json/output.json', 'a', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, ensure_ascii=False, indent=4)




if __name__ == "__main__":
    run_pipeline()