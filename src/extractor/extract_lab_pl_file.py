from typing import List, Tuple, Dict
from xml.etree.ElementTree import Element


def qname(tag: str, nsmap: Dict[str, str]) -> str:
    """Funkcja zamienia skróconą nazwę tagu XML z prefixem na pełną nazwę z przestrzenią nazw, zgodną ze składnią
    biblioteki xml.etree.ElementTree."""

    prefix, local = tag.split(":")
    return f"{{{nsmap[prefix]}}}{local}"


def extract_lab_pl_labels_and_values(lab_pl_parsed: Element, lab_pl_namespaces: Dict[str, str]) -> List[
    Tuple[str, str]]:
    """Funkcja została stworzona w celu wyodrębnienia powiązań między etykietami (labelami) a ich opisami tekstowymi.
       Pozwala to ustalić, która etykieta odpowiada jakiej wartości, co jest niezbędne do dalszego przetwarzania danych.
       Informacje te są wykorzystywane do zbudowania pełnej struktury formularza w kolejnych etapach przetwarzania."""

    label_dict: Dict[str, str] = {}
    for label in lab_pl_parsed.findall(f'.//{qname("label:label", lab_pl_namespaces)}'):
        label_id = label.attrib[f'{{{lab_pl_namespaces["xlink"]}}}label']
        label_text = label.text
        label_dict[label_id] = label_text
    label_dict = {k: v for k, v in label_dict.items() if k.count('_') != 3}
    loc_dict: Dict[str, str] = {}
    for loc in lab_pl_parsed.findall(f'.//{qname("link:loc", lab_pl_namespaces)}'):
        label_id = loc.attrib[f'{{{lab_pl_namespaces["xlink"]}}}label']
        href = loc.attrib[f'{{{lab_pl_namespaces["xlink"]}}}href']
        loc_dict[label_id] = href.split('#')[-1]

    labels_and_values: List[Tuple[str, str]] = []
    for arc in lab_pl_parsed.findall(f'.//{qname("gen:arc", lab_pl_namespaces)}'):
        from_label = arc.attrib[f'{{{lab_pl_namespaces["xlink"]}}}from']
        to_label = arc.attrib[f'{{{lab_pl_namespaces["xlink"]}}}to']
        if from_label in loc_dict and to_label in label_dict:
            labels_and_values.append((loc_dict[from_label], label_dict[to_label]))
    return labels_and_values
