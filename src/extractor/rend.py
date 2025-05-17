

def extract_rend_file(root):
    labels = []
    for elem in root.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            labels.append(elem.attrib['id'])
        if elem.tag.endswith('tableBreakdownArc') and 'axis' in elem.attrib:
            labels.append(elem.attrib['axis'])

    labels = [elem for elem in labels if not elem.startswith('uknf_a')]
    print(labels)
    return labels

def extract_rend_file_labels_and_qnames(root):
    labels_and_qnames = []
    for elem in root.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            rule_id = elem.attrib['id']
            for qname_elem in elem.iter():
                if qname_elem.tag.endswith('qname'):
                    labels_and_qnames.append([rule_id, qname_elem.text])
    return labels_and_qnames