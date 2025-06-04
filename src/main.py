import os

import requests

from create_json_structure.json_structure import create_structure
from src.config.constants import BASE_URL, MENU, DIRECTORIES
from src.extractor.extract_report import generate_json_reports


def create_directory():
    """Funkcja podczas włączenia programu tworzy wszystkie potrzebne katalogi do przechowywania danych."""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)


def run_pipeline() -> None:
    """Głowna funkcja realizująca generowanie struktury bazodanowej, ekstrakcji danych z raportów oraz ładowanie tych
    danych do bazy. Po uruchmieniu zostaną stworzone wszystkie potrzebne katalogi."""

    create_directory()

    action = None
    while action != "0":
        print(MENU)
        action = input("Akcja: ")
        match action:
            case "0":
                print("Koniec programu")
            case "1":
                create_structure()
                input("Naciśnij Enter, aby kontynuować...")
            case "2":
                generate_json_reports()
                input("Naciśnij Enter, aby kontynuować...")
            case "3":
                response = requests.post(f"{BASE_URL}/load/structure")
                print(f"Status: {response.status_code}, odpowiedź: {response.text}")
                input("Naciśnij Enter, aby kontynuować...")
            case "4":
                response = requests.post(f"{BASE_URL}/load/reports")
                print(f"Status: {response.status_code}, odpowiedź: {response.text}")
                input("Naciśnij Enter, aby kontynuować...")
            case _:
                print("Nieznana akcja")
                input("Naciśnij Enter, aby kontynuować...")
        print("/////////////////////////////////////////////////////////////////////////")
        print("/////////////////////////////////////////////////////////////////////////")
        print("/////////////////////////////////////////////////////////////////////////")


if __name__ == "__main__":
    run_pipeline()
