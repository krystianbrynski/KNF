
def extract_tab_col(columns0,tabels9,headers):
    dict_col_tab = {}
    tabels = []
    columns = []

    if len(tabels9) == 0:  # jesli nie ma tabeli czyli tabela to nagłowek
        for col in columns0:
            columns.append(col[1])
        dict_col_tab[headers] = columns
        tabels.append(headers)

    else:
        if len(tabels9) == 1:  # jesli tabela jest tylko jedna ladujemy wszystkie kolumny do jedenj tabeli
            for col in columns0:
                columns.append(col[1])
            dict_col_tab[tabels9[1]] = columns
            tabels.append([tabels9[1]])
        else:  # jesli jest wiecej tabel musimy ladowac przedzialami, do kazdego przedzialu z tabeli wpadaja kolumny
            for col in range(0, len(tabels9)):
                start = int(tabels9[col][2])
                tabela = tabels9[col][1]
                kolumny = []
                if col != len(tabels9) - 1:
                    stop = int(tabels9[col + 1][2])
                    for i in columns0:
                        wartosc = int(i[2])
                        if wartosc > start and wartosc < stop:
                            kolumny.append(i[1])
                    dict_col_tab[tabela] = kolumny
                    tabels.append(tabela)
                else:
                    for i in columns0:
                        wartosc = int(i[2])
                        if wartosc > start:
                            kolumny.append(i[1])
                    dict_col_tab[tabela] = kolumny
                    tabels.append(tabela)
    return dict_col_tab, tabels
