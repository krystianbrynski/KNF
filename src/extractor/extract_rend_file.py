from xml.etree.ElementTree import Element
from typing import List, Tuple


def extract_rend_ordered_labels_and_axes(rend_parsed: Element) -> List[str]:
    """Funkcja została stworzona, aby wyodrębnić kolejność etykiet i osi z pliku XML, w takiej kolejności,
       w jakiej występują w pliku. Dzięki temu możemy łatwo rozróżnić, które etykiety należą do osi x,
       a które do osi y."""

    labels: List[str] = []
    for elem in rend_parsed.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            labels.append(elem.attrib['id'])
        if elem.tag.endswith('tableBreakdownArc') and 'axis' in elem.attrib:
            labels.append(elem.attrib['axis'])

    labels = [elem for elem in labels if not elem.startswith('uknf_a')]
    return labels


def extract_rend_labels_and_qnames(rend_parsed: Element) -> List[Tuple[str, str]]:
    """Funkcja wyodrębnia powiązania pomiędzy identyfikatorami etykiet a nazwami kwalifikowanymi (qname).
    Te powiązania są niezbędne, ponieważ pozwalają zrozumieć, które etykiety (labels) odpowiadają
    konkretnym nazwom kwalifikowanym (qname). Dzięki temu możliwe jest późniejsze dopasowanie
    typu danych do odpowiednich etykiet, bazując właśnie na qname."""

    labels_and_qnames: List[Tuple[str, str]] = []
    for elem in rend_parsed.iter():
        if elem.tag.endswith('ruleNode') and 'id' in elem.attrib:
            rule_id = elem.attrib['id']
            for qname_elem in elem.iter():
                if qname_elem.tag.endswith('qname'):
                    labels_and_qnames.append((rule_id, qname_elem.text))

    return labels_and_qnames
