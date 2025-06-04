# Generowanie struktury bazy danych na podstawie taksonomii oraz rozładunek danych do tej bazy

## Cel Projektu

Celem projektu jest opracowanie i wdrożenie zautomatyzowanego procesu przygotowania i przetwarzania danych raportowych oraz taksonomii.

## Zrealizowane zadania

- Generowanie plików transportowych na podstawie raportu oraz ich załadunek do bazy danych  
- Generyczne tworzenie struktury bazy danych na podstawie modelu taksonomii (TaksonomiaBION)  
- Opracowanie skryptów w języku Python, które realizują powyższe zadania


## Instalacja bibliotek 

Zainstaluj wymagane zależności i biblioteki za pomocą poniższego polecenia:

```pip install -r .\requirements.txt```

## Tworzenie katalogów

Aby stworzyć potrzebne katalogi należy uruchomic skrypt src/main.py. Skrypt ten automatycznie utworzy wszystkie niezbędne katalogi.
W terminalu skorzystaj z polecenia:

```python src/main.py```

## Użycie programu

Po uruchomieniu programu src/main.py w terminalu wyświetli się menu dla użytkownika, a zaraz po nim prośba o wybranie numeru akcjii.

```
 === MENU PROGRAMU ===
        Wybierz jedną z opcji:

        1 - Tworzenie struktury bazodanowej na podstawie taksonomii
        2 - Ekstrakcja danych z raportu
        3 - Ładowanie struktury bazodanowej do bazy danych
        4 - Ładowanie danych z raportu do bazy danych
        0 - Wyjście z programu

        =====================

Akcja:
```


** 1. Tworzenie struktury bazodanowej na podstawie taksonomii.**

Do powstałego katalogu data/taxonomy należy wrzucić model taksonomii, przed wybraniem akcjii. 

```
input
KNF/
├───data/
│   ├───taxonomy/
│       └───Taxonomy
```

Po wrzuceniu modelu taksonomii można w terminalu wpisać wartość 1, aby uruchomić skrypt realizujący to zadanie.

```
output
KNF/
├───structure/
│   ├───full_structure/
│   │   ├───form_name_1.json
│   │   ├───form_name_2.json
│   │   └───form_name_3.json
│   └───taxonomy_info/
│   │   ├───taxonomy_info.json
```

Skrypt, na podstawie Twojej taksonomii, wygeneruje pliki transportowe. Plików transportowych (zawierających strukture dla danego arkusza) będzie tyle ile arkuszy znajduje się we wszystkich formularzach. Każdy plik zostanie zapisany w formacie JSON i nazwany zgodnie z nazwą odpowiadającego mu arkusza. Skrypt również zapisze plik taxonomy_info.json do katalogu taxonomy_info wraz z nazwą oraz wersją taksonomii

** 2. Ekstrakcja danych z raportu.**

Do katalogu data/reports należy wrzucić jeden raport w formacie '.xls' lub '.xlsx' z uzupełnionymi danymi, przed wykonaniem akcjii.


```
input
KNF/
├───data/
│   ├───reports/
│       └───report.xlsx
```

Po wrzuceniu raportu można w terminalu wpisać wartość 2, aby uruchomić skrypt.

```
output
KNF/
├───report_data/
│   │   ├───sheet_name1.json
│   │   ├───sheet_name2.json
│   │   └───sheet_name3.json
```

Skrypt na podstawie wrzuconego raportu wyekstraktuje dane z raportu oraz utworzy tyle plików transportowych ile jest arkuszy w  danym formularzu.

** 3. Ładowanie struktury bazodanowej do bazy danych.**

Przed załadunkiem struktury bazodanowej trzeba najpierw wykonać akcję nr 1, aby utworzyć pliki transportowe (pełną strukturę dla taksonomii zapisaną w formatach JSON).
Należy uruchomić api w terminalu, jeśli tego jeszcze nie zrobiłeś.

```uvicorn src.api_interface.api:app --reload```

po poprawnym uruchomieniu dostaniemu informację: "INFO:     Application startup complete".
Teraz możemy uruchomić akcję i wpisać w terminal wartość 3.
Skrypt załaduje Twoją strukture do bazy danych i wyświetli w terminalu komunikat:
"Struktura została załadowana do bazy danych", jeśli operacja zakończy się sukcesem.

** 4. Ładowanie danych z raportu do bazy danych.**

Przed załadunkiem danych do bazy danych, upewnij się że wykonałeś akcje 2, która wyekstraktuje twoje dane z raportu i zapisze pliki transportowe.
Należy uruchomić api w terminalu, jeśli tego jeszcze nie zrobiłeś.

```uvicorn src.api_interface.api:app --reload```

po poprawnym uruchomieniu dostaniemu informację: "INFO:     Application startup complete".
Teraz możemy uruchomić akcję i wpisać w terminal wartość 4.
Skrypt załaduje twoje wyekstraktowane dane do bazy danych i wyświetli w terminalu komentarz:
"Raport został pomyślnie rozładowany do bazydanych", jeśli operacja zakończy się sukcesem.

** 0 - Wyjście z programu.**

Wybierz akcje 0 jeśli chcesz zakończyć program





