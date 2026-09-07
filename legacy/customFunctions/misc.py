import os
from typing import Union

def pathfinder(dirname='.') -> dict[str, Union[str, int]]:
    """
    This a function that returns a dictionary of paths for specific elements of the project
    """
    paths = {
        "csv_table" : 0,
        "database" : 0,
    }
    filenames = os.listdir(dirname)
    for filename in filenames:
        filename = os.path.join(dirname, filename)
        extension = os.path.splitext(filename)[1]
        # Находим файл с таблицой
        if extension in ['.csv', '.xlsx']:
            paths["csv_table"] = filename
        # Проверяем, есть ли готовая датабаза
        if extension == '.db':
            paths["database"] = filename
        
    return paths