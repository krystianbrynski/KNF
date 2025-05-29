from xml.etree.ElementTree import Element
from typing import List, Tuple

# Funkcja została stworzona, aby automatycznie wykrywać przestrzeń nazw (namespace)
# używaną w atrybutach typu "label". Jest to niezbędne do poprawnego odczytu danych
# z atrybutów XML, które zawierają prefiksy przestrzeni nazw.
def extract_namespace(lab_codes_parsed: Element)-> str:
    namespace = ""
    for elem in lab_codes_parsed.iter():
        for attr in elem.attrib:
            if namespace:
                break
            if "label" in attr:
                namespace = attr.split("}")[0] + "}"
                break
    return namespace


# Funkcja została stworzona, aby wyodrębnić z pliku XML powiązania między etykietami (labels) a ich wartościami (data points).
# Dzięki temu można dokładnie określić, jaki konkretny punkt danych (data point) jest przypisany do której etykiety.
def extract_lab_codes_labels_and_values(lab_codes_parsed: Element)-> List[Tuple[str, str]]:
    namespace = extract_namespace(lab_codes_parsed)
    labels_and_value: List[Tuple[str, str]] = []

    for label in lab_codes_parsed.findall(".//{*}label"):
        label_attr = label.get(f"{namespace}label")
        label_value = label.text.strip()

        if label_attr and "uknf_c" in label_attr:
            clean_label = label_attr.replace("label_", "")
            labels_and_value.append((clean_label, label_value))

    return labels_and_value
