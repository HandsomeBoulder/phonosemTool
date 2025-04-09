# Модуль парсинга excel таблиц
import pandas as pd
# Модуль для работы с операционной системой
import os
# Модуль для работы с датабазой
import sqlite3
# Кастомные функции
from customFunctions.misc import *

# Ф-ция компиляции SQLite датабазы
def main() -> None:
    """
    This is a function that parses csv table and inserts its values into SQLite database
    """
    # Директория, где хранятся материалы, необходимы для работы алгоритмов
    dirname, db_name = 'materials', 'phonosemantic.db'
    # Поиск csv таблицы и датабазы с использованием кастомной ф-ции на основе модуля OS
    paths = pathfinder(dirname=dirname)
    excel_table, database = paths["csv_table"], paths["database"]
    # Проверяем наличие таблицы
    if not excel_table:
        # Если таблицы нет, печатаем ошибку и выходим
        print("Csv table is not detected. Exiting...")
        exit()
    # Проверяем наличие ДБ
    if database:
        # Если датабаза уже есть, предлагаем удалить или оставить старую
        while True:
            response = input('Database already exists, delete? (y/n) ').strip().lower()
            if response == 'y':
                os.remove(database)
                print('Old database deleted')
                break
            elif response == 'n':
                print('Exiting...')
                exit()
            else:
                print('Invalid input. Try again')

    print("Compiling database...")

    # Подключаемся к датабазе
    conn = sqlite3.connect(os.path.join(dirname, db_name))
    cursor = conn.cursor()

    # Создаем таблицу для глаголов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verbs (
    id INTEGER PRIMARY KEY,
    verb TEXT NOT NULL,
    transcription TEXT NOT NULL,
    category TEXT NOT NULL,
    meaning TEXT NOT NULL
    )
    ''')

    # Создаем таблицу для переводов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS translations (
    id INTEGER PRIMARY KEY,
    parentId INTEGER NOT NULL,
    word TEXT NOT NULL,
    transcription TEXT NOT NULL,
    FOREIGN KEY (parentId) REFERENCES verbs(id) ON DELETE CASCADE
    )
    ''')

    # Применяем изменения
    conn.commit()

    # Читаем csv таблицу
    df = pd.read_csv(excel_table)
    # Опускаем все пустые строки
    df.dropna(inplace = True)
    # Производим операции над каждой строкой csv таблицы
    for row in df.itertuples():
        # Получаем элементы строки
        word, category, meaning = row.verb.strip(), row.category.strip(), row.meaning.strip()
        # Получаем и предобрабатываем английскую транскрипцию
        transcriptionEn = row.transcriptionEn.replace('/', '').replace('.', '').strip()
        # Вносим данные в таблицу глаголов
        cursor.execute("INSERT INTO verbs (verb, transcription, category, meaning) VALUES (?, ?, ?, ?)", 
                        (word, transcriptionEn, category, meaning))
        # Собираем данные для таблицы переводов
        parent = cursor.lastrowid  # Получаем ID родителя
        # Получаем и парсим списки переводов и транскрипций переводов
        translations = row.translation.split(',')
        transcriptionsRu = row.transcriptionRu.split(',')
        # Для каждого глагола движения вносим в таблицу переводов каждый эквивалент и его транскрипцию
        for translation, transcriptionRu in zip(translations, transcriptionsRu):
            translation, transcriptionRu = translation.strip().lower(), transcriptionRu.replace('/', '').replace('.', '').strip()
            cursor.execute("INSERT INTO translations (parentId, word, transcription) VALUES (?, ?, ?)", 
                            (parent, translation, transcriptionRu))

    # Применяем изменения и закрываем подключение к ДБ
    conn.commit()
    conn.close()

    # Уведомление об успешном завершении
    print(f'Database successfully compiled with {parent} verbs total')

# Запуск функции
if __name__ == '__main__':
    main()