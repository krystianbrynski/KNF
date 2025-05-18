# Generator struktur danych i szablonów plików na podstawie taksonomii EBA

## Opis projektu

Projekt umożliwia automatyczne generowanie:

1. Szablonów plików transportowych w formatach:
   - ?

2. Struktury bazy danych odpowiadającej modelowi danych zawartemu w taksonomii EBA.

Wejściem do programu jest **TaxonomiaBIon** — taksonomia EBA w postaci plików XML, dostarczanych lokalnie lub pobieranych ze strony [EBA](https://www.eba.europa.eu/).

## Funkcjonalność

- Parsowanie plików XML z taksonomii
- Generowanie struktur JSON dla każdego arkusza formularza
- Generowanie struktury bazy danych
- Tworzenie szablonów plików transportowych (?)
- Ładowanie plików transportowych do bazy danych

## Technologie

- Python
- `xml.etree.ElementTree` — biblioteka do parsowania plików XML
- `pathlib.Path` — obiektowa obsługa ścieżek plików w Pythonie
- `json` — zapis struktury danych w formacie JSON
- `os` — operacje na plikach i ścieżkach systemowych


## Tworzenie struktury bazy danych

### 1. Ekstrakcja danych i generowanie struktur JSON

- Inputem do programu jest **TaxonomiaBIon** – zestaw plików XML opisujących strukturę formularzy, wraz z typami danych i metrykami.
- Skrypt przechodzi przez wszystkie foldery, w których znajdują się definicje formularzy, a następnie analizuje każdy formularz oraz każdy arkusz w ramach formularza.
- Pliki XML są przetwarzane z użyciem biblioteki `xml.etree.ElementTree`, a następnie analizowane przez logikę programu.
- Dla każdego formularza i każdego arkusza w tym formularzu generowany jest osobny plik JSON opisujący strukturę danych.


#### Struktura wygenerowanego JSON-a

```text
{
  "nazwa_formularza": {
    "uknf_cXX": {
      "rows": [...],
      "data_point": [...],
      "cols": [...],
      "datatype": "...",
      "qname": "...",
      "report_name": "..."
    }
  }
}
```

## Opis pól:

| Pole            | Opis |
|----------------|-------------------------------------------|
| **nazwa_formularza** | Nazwa formularza jako główny klucz |
| **uknf_cXX** | Unikalny klucz/label dla wiersza |
| **rows** | Wartość wiersza |
| **data_point** | Przecięcie wiersza i kolumny np. 0010X0010 |
| **cols** | Lista wartości kolumn |
| **datatype** | Typ danych |
| **qname** | Nazwa metryki |
| **report_name** | Nazwa arkusza w formularzu |

### 2. Ładowanie plików JSON do bazy danych MS SQL

- Marta doda
