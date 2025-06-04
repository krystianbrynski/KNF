from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


def parse_xml(path: str) -> Element:
    """Funkcja została stworzona, aby wielokrotnie i wygodnie parsować różne pliki XML,
    eliminując powtarzanie kodu i zapewniając spójny sposób uzyskiwania dostępu do danych XML."""

    tree = ET.parse(path)
    return tree.getroot()
