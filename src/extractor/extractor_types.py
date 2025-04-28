import xml.etree.ElementTree as ET


def extract_types(path_file):
    tree = ET.parse(path_file)
    root = tree.getroot()

    named_types_list = []

    for elem in root.iter():
        if elem.tag.endswith('element'):
            name = elem.attrib.get('name')
            typ = elem.attrib.get('type')
            if name and typ:
                named_types_list.append((name, typ))

    return named_types_list
