import requests

from create_json_structure.json_structure import create_structure
from src.config.constants import BASE_URL, MENU
from src.extractor.extract_report import generate_json_reports


def run_pipeline() -> None:
    '''Głowna funkcja realizująca generowanie struktury bazodanowej, ekstrakcji danych z raportów oraz ładowanie tych danych do bazy.
    Przed uruchmieniem upewnij się, że wrzuciłeś model taksonomi oraz raport oraz czy stworzyłeś zgodnie z dokumentacją techniczną potrzebne katalogi, jeśli nie istnieją'''
    akcja = None
    while akcja != "0":
        print(MENU)
        akcja = input("Akcja: ")
        match akcja:
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
