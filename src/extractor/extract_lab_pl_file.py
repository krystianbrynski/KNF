#  Funkcja zamienia skróconą nazwę tagu XML z prefixem na pełną nazwę z przestrzenią nazw, zgodną ze składnią biblioteki xml.etree.ElementTree.
def qname(tag, nsmap):
    prefix, local = tag.split(":")
    return f"{{{nsmap[prefix]}}}{local}"

#  Funkcja zwraca listę krotek (label_id, label_text), gdzie label_id to wyciągnięty identyfikator
#  (część po '#' z atrybutu href lokalizacji), a label_text to odpowiadający mu tekst etykiety.
def extract_lab_pl_labels_and_values(root, namespaces):
    label_dict = {}
    for label in root.findall(f'.//{qname("label:label", namespaces)}'):
        label_id = label.attrib[f'{{{namespaces["xlink"]}}}label']
        label_text = label.text
        label_dict[label_id] = label_text

    loc_dict = {}
    for loc in root.findall(f'.//{qname("link:loc", namespaces)}'):
        label_id = loc.attrib[f'{{{namespaces["xlink"]}}}label']
        href = loc.attrib[f'{{{namespaces["xlink"]}}}href']
        loc_dict[label_id] = href.split('#')[-1]

    labels_and_values = []
    for arc in root.findall(f'.//{qname("gen:arc", namespaces)}'):
        from_label = arc.attrib[f'{{{namespaces["xlink"]}}}from']
        to_label = arc.attrib[f'{{{namespaces["xlink"]}}}to']
        if from_label in loc_dict and to_label in label_dict:
            labels_and_values.append((loc_dict[from_label], label_dict[to_label]))

    return labels_and_values
