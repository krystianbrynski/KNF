# Funkcja, która zbiera pary (name, typ) z dokumentu XML
# name - nazwa metryki
# typ - typ danych
def extract_types_and_names(met_parsed):
    data_types_with_names = []

    for elem in met_parsed.iter():
        if elem.tag.endswith('element'):
            name = elem.attrib.get('name')
            typ = elem.attrib.get('type')
            if name and typ:
                data_types_with_names.append((name, typ))
    return data_types_with_names