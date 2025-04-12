import xml.etree.ElementTree as ET

ns = {
    "link": "http://www.xbrl.org/2003/linkbase",
    "xlink": "http://www.w3.org/1999/xlink",
    "label": "http://xbrl.org/2008/label",
    "gen": "http://xbrl.org/2008/generic"
}


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
        arcs[from_label] = to_label

    locators = {}
    for loc in root.findall(".//link:loc", ns):
        loc_label = loc.get("{http://www.w3.org/1999/xlink}label")
        href = loc.get("{http://www.w3.org/1999/xlink}href")
        if href:
            locators[loc_label] = href.split("#")[-1]

    href_to_text = {}
    for from_label, to_label in arcs.items():
        href_id = locators.get(from_label)  # np. "uknf_c32"
        text = labels.get(to_label)  # np. "Imię" lub "0010"
        if href_id and text:
            href_to_text[href_id] = text

    return href_to_text


file_lab_codes = r"D:\Pycharm\Pierwszyprogram\KNF1\data\taxonomy\TaksonomiaBION\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\fws\bion\bion-2024-12\2024-10-21\tab\n.rr.bk.01.02\n.rr.bk.01.02-lab-codes.xml"
file_lab_pl = r"D:\Pycharm\Pierwszyprogram\KNF1\data\taxonomy\TaksonomiaBION\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\fws\bion\bion-2024-12\2024-10-21\tab\n.rr.bk.01.02\n.rr.bk.01.02-lab-pl.xml"

pl_dict = parse_label_file(file_lab_pl, ns)
codes_dict = parse_label_file(file_lab_codes, ns)

unified = {}
all_ids = set(pl_dict.keys()) | set(codes_dict.keys())
for href_id in all_ids:
    pl_text = pl_dict.get(href_id)
    code_text = codes_dict.get(href_id)
    unified[href_id] = (pl_text, code_text)

columns_ending_0 = {}
columns_ending_9 = {}

for href_id, (pl_text, code_text) in unified.items():
    if not href_id.startswith("uknf_c"):
        continue

    if code_text:
        if code_text.endswith("0"):
            columns_ending_0[href_id] = (pl_text, code_text)
        elif code_text.endswith("9"):
            columns_ending_9[href_id] = (pl_text, code_text)

sorted_columns_0 = sorted(columns_ending_0.items(), key=lambda item: item[1][1])
sorted_columns_9 = sorted(columns_ending_9.items(), key=lambda item: item[1][1])
sorted_cols_0_list = [(href_id, text_pl, text_code) for href_id, (text_pl, text_code) in sorted_columns_0]
sorted_cols_9_list = [(href_id, text_pl, text_code) for href_id, (text_pl, text_code) in sorted_columns_9]

for href_id, (text_pl, text_code) in unified.items():
    if href_id.startswith("uknf_tN"):
        headers = text_pl

kolumny_wynik = []
tabele_wynik = []

if len(columns_ending_9) == 0:
    for col in sorted_cols_0_list:
        kolumny_wynik.append(col[1])
    tabele_wynik.append(headers)
    print("kolumny", kolumny_wynik)
    print("tabele", tabele_wynik)

else:
    for col in sorted_cols_0_list:
        kolumny_wynik.append(col[1])
    for col in sorted_cols_9_list:
        tabele_wynik.append(col[1])
    print("kolumny", kolumny_wynik)
    print("tabele", tabele_wynik)
