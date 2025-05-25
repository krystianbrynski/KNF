# Funkcja, która w kolejności występowania w pliku XML
# wyciąga wartości atrybutów 'id' z elementów 'ruleNode'
# oraz wartości atrybutów 'axis' z elementów 'tableBreakdownArc'.
# Zwraca listę wszystkich tych wartości, pomijając te, które zaczynają się od 'uknf_a'.
# Przykładowy wynik to lista takich wartości:
# ['uknf_c2', 'uknf_c3', 'uknf_c4', 'x', 'uknf_c9', 'uknf_c6', 'uknf_c7', 'uknf_c8', 'y']
# Dzięki zachowaniu kolejności łatwo później dopasować, które etykiety (labels) należą do konkretnego axis (x lub y).
def extract_rend_ordered_labels_and_axes(rend_parsed):
    labels = []
    for elem in rend_parsed.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            labels.append(elem.attrib['id'])
        if elem.tag.endswith('tableBreakdownArc') and 'axis' in elem.attrib:
            labels.append(elem.attrib['axis'])

    labels = [elem for elem in labels if not elem.startswith('uknf_a')]
    return labels


# Funkcja, która wyciąga identyfikatory elementów (id) oraz powiązane z nimi nazwy kwalifikowane (qname)
def extract_rend_labels_and_qnames(rend_parsed):
    labels_and_qnames = []
    for elem in rend_parsed.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            rule_id = elem.attrib['id']
            for qname_elem in elem.iter():
                if qname_elem.tag.endswith('qname'):
                    labels_and_qnames.append([rule_id, qname_elem.text])
    return labels_and_qnames