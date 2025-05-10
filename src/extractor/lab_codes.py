
def extract_namespace(root):
    namespace = None
    for elem in root.iter():
        for attr in elem.attrib:
            if namespace:
                break
            if "label" in attr:
                namespace = attr.split("}")[0] + "}"
                break
    return namespace


def extract_lab_codes_file(root):
    namespace = extract_namespace(root)

    labels_and_value = []
    for label in root.findall(".//{*}label"):
        label_attr = label.get(f"{namespace}label")
        label_value = label.text.strip() if label.text else None

        if label_attr and "uknf_c" in label_attr:
            clean_label = label_attr.replace("label_", "")
            labels_and_value.append((clean_label, label_value))

    return labels_and_value
