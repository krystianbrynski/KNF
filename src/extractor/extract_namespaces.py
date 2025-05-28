import xml.etree.ElementTree as ET
from typing import Dict


# Funkcja została stworzona, aby wyodrębnić wszystkie przestrzenie nazw (namespaces) z pliku XML
def extract_namespaces(xml_file: str) -> Dict[str, str]:
    events = "start", "start-ns"
    ns_map = {}
    for event, elem in ET.iterparse(xml_file, events):
        if event == "start-ns":
            prefix, uri = elem
            ns_map[prefix] = uri
        elif event == "start":
            break

    return ns_map
