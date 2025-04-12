import json

data = {
    'Sporządził(a):': ['Imię', 'Nazwisko', 'telefon', 'e-mail'], 'Zatwierdził(a):': ['Imię', 'Nazwisko', 'telefon', 'e-mail'], 'Audyt Wewnętrzny:': ['Imię', 'Nazwisko', 'telefon', 'e-mail'], 'Komórka ds. zgodności:': ['Imię', 'Nazwisko', 'telefon', 'e-mail']}

output_file = "C:/Users/marta/PycharmProjects/KNF/create_db/przyklad.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)