import os

PATH = r'../data/taxonomy/TaksonomiaBION/www.uknf.gov.pl/pl/fr/xbrl/fws/bion/bion-2024-12/2024-10-21/tab'

def search_paths(target_folders):
    paths = []
    for folder in target_folders:
        folder_path = os.path.join(PATH, folder)
        if os.path.isdir(folder_path):  # Sprawdzenie, czy folder istnieje
            paths.append(folder_path)
    return paths

def aim_paths(paths):
    aim_paths = []
    for path in paths:
        if os.path.isdir(path):
            list= []
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    full_path = full_path.replace("\\", "/")
                    if 'lab-pl' in file_name:
                        list.append(full_path)
                    elif 'rend' in file_name:
                        list.append(full_path)
                    elif 'lab-codes' in file_name:
                        list.append(full_path)
            aim_paths.append(list)

    return aim_paths