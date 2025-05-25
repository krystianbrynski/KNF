# Funkcja, która z podanego korzenia XML szuka przestrzeni nazw (namespace)
# na podstawie atrybutów zawierających słowo "label" i zwraca ją w formacie '{namespace}'
def extract_namespace(lab_codes_parsed):
    namespace = None
    for elem in lab_codes_parsed.iter():
        for attr in elem.attrib:
            if namespace:
                break
            if "label" in attr:
                namespace = attr.split("}")[0] + "}"
                break
    return namespace


# Funkcja, która z podanego korzenia XML wyciąga wszystkie elementy <label>,
# których atrybut 'label' zawiera ciąg "uknf_c".
# Zwraca listę krotek (label, wartość), gdzie:
# - label to oczyszczony atrybut 'label' (usunięty prefiks "label_"),
# - wartość to tekst zawarty w elemencie <label>
def extract_lab_codes_labels_and_values(lab_codes_parsed):
    namespace = extract_namespace(lab_codes_parsed)

    labels_and_value = []
    for label in lab_codes_parsed.findall(".//{*}label"):
        label_attr = label.get(f"{namespace}label")
        label_value = label.text.strip() if label.text else None

        if label_attr and "uknf_c" in label_attr:
            clean_label = label_attr.replace("label_", "")
            labels_and_value.append((clean_label, label_value))

    return labels_and_value
