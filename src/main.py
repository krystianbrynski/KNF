from parser.parse_file import parse_label_file
from src.extractor.extract_two_files import extract_from_pl_codes
from src.extractor.extract_tab_col import extract_tab_col
from config import config

FILE_LAB_CODES = config.FILE_LAB_CODES
FILE_LAB_PL = config.FILE_LAB_PL
NS = config.NS


def run_pipeline() -> None:
    pl_dict = parse_label_file(FILE_LAB_PL, NS)
    codes_dict = parse_label_file(FILE_LAB_CODES, NS)
    columns0, tabels9, headers = extract_from_pl_codes(pl_dict, codes_dict)

    dict_tab_col, name_of_tabels = (extract_tab_col(columns0, tabels9, headers))

    print("Słownik, klucz tabela + wartosci kolumn:", dict_tab_col)
    print("///////////////////////////////////////////")
    print("Nazwa tabel które są w słowniku:", name_of_tabels)


if __name__ == "__main__":
    run_pipeline()
