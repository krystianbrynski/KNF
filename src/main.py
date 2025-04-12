from parser.parse_file import parse_label_file
from src.extractor.extract_two_files import extract_from_pl_codes
from src.extractor.extract_tab_col import extract_tab_col

FILE_LAB_CODES = r"D:\Pycharm\Pierwszyprogram\KNF1\data\taxonomy\TaksonomiaBION\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\fws\bion\bion-2024-12\2024-10-21\tab\n.rr.bk.01.00\n.rr.bk.01.00-lab-codes.xml"
FILE_LAB_PL = r"D:\Pycharm\Pierwszyprogram\KNF1\data\taxonomy\TaksonomiaBION\TaksonomiaBION\www.uknf.gov.pl\pl\fr\xbrl\fws\bion\bion-2024-12\2024-10-21\tab\n.rr.bk.01.00\n.rr.bk.01.00-lab-pl.xml"

NS = {
    "link": "http://www.xbrl.org/2003/linkbase",
    "xlink": "http://www.w3.org/1999/xlink",
    "label": "http://xbrl.org/2008/label",
    "gen": "http://xbrl.org/2008/generic"
}


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
