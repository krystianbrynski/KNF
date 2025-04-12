import xml.etree.ElementTree as ET


def parse_label_file(file_path, ns):
    tree = ET.parse(file_path)
    root = tree.getroot()

    labels = {}
    for label in root.findall(".//label:label", ns):
        lab_id = label.get("{http://www.w3.org/1999/xlink}label")
        if label.text:
            labels[lab_id] = label.text.strip()

    arcs = {}
    for arc in root.findall(".//gen:arc", ns):
        from_label = arc.get("{http://www.w3.org/1999/xlink}from")
        to_label = arc.get("{http://www.w3.org/1999/xlink}to")
        if to_label.count('_') == 3:  # zadac pytanie czemu tak jest o co chodzi?????
            continue
        arcs[from_label] = to_label

    locators = {}
    for loc in root.findall(".//link:loc", ns):
        loc_label = loc.get("{http://www.w3.org/1999/xlink}label")
        href = loc.get("{http://www.w3.org/1999/xlink}href")
        if href:
            locators[loc_label] = href.split("#")[-1]

    href_to_text = {}
    for from_label, to_label in arcs.items():
        href_id = locators.get(from_label)
        text = labels.get(to_label)
        if href_id and text:
            href_to_text[href_id] = text

    return href_to_text
