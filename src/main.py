import xml.etree.ElementTree as ET
path_file = "C:/Users/marta/PycharmProjects/KNF/data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/dict/met/met.xsd"

tree = ET.parse(path_file)
root = tree.getroot()

wyniki = []

for elem in root.iter():
    if elem.tag.endswith('element'):
        name = elem.attrib.get('name')
        typ = elem.attrib.get('type')
        if name and typ:
            wyniki.append((name, typ))

for name, typ in wyniki:
    print(f"Nazwa: {name}, Typ: {typ}")