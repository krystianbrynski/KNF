import xml.etree.ElementTree as ET

def extract_namespaces(xml_file):
    events = "start", "start-ns"
    ns_map = {}
    for event, elem in ET.iterparse(xml_file, events):
        if event == "start-ns":
            prefix, uri = elem
            ns_map[prefix] = uri
        elif event == "start":
            break
    return ns_map