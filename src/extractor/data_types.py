
def extract_types(root):
    named_types_list = []

    for elem in root.iter():
        if elem.tag.endswith('element'):
            name = elem.attrib.get('name')
            typ = elem.attrib.get('type')
            if name and typ:
                named_types_list.append((name, typ))

    return named_types_list