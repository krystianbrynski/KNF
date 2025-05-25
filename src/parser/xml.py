import xml.etree.ElementTree as ET


# Funkcja, która zwraca sparsowany plik XML
def parse_xml(path):
    tree = ET.parse(path)
    return tree.getroot()
