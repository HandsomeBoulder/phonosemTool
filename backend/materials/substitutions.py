# Библиотека регулярных выражений
import re
# Библиотека для работы с xlsx и csv таблицами
import pandas as pd

# Функция, производящая замены
def substitute(csv='verbs.csv') -> None:
    """
    This is a function that performs symbol substitutions
    in a csv table to produce relevant russian transcriptions
    """
    # Символы русской транскрипции по Богдановой
    allowed_char = ":ˈ’aieыoubpvfgkxdtjžšzslmnrcč"
    # Словарь замен
    replacements = {
        # вспомогательные символы
        'ʲ' : '’',
        # гласные
        'а' : 'a',
        'ɐ' : 'a',
        'ɑ' : 'a',
        'ɪ' : 'i',
        'ɔ' : 'o',
        'ʉ' : 'u',
        'ə' : 'a',
        'ɨ' : 'ы',
        'ʊ' : 'u',
        'æ' : 'a',
        'ɛ' : 'e',
        'о' : 'o',
        '’ɵ' : '’o',
        # согласные
        'ɫ' : 'l',
        'ɡ' : 'g',
        't͡s' : 'c',
        'ts' : 'c',
        'ɕɕʲ' : 'š’',
        'ɕː' : 'š’',
        't͡ɕ' : 'č',
        'tɕ' : 'č',
        'ɕ' : 'š',
        'ʐ' : 'ž',
        'ʂ' : 'š',
        'ʃ' : 'š',
        # вспомогательные символы
        'ː' : '',
        ':' : ''
    }
    # Правки, внесенные после замен
    remarks = {
        r'tsa\b' : 'ca',
        r't’s’a\b' : 'ca',
        r't’sa\b' : 'ca',
        r'ts’a\b' : 'ca'
    }
    flag = True
    # Импорт транскрипции
    df = pd.read_csv(csv, encoding='utf-8')
    # Опускаем пустые строки
    df.dropna(inplace = True)
    # Получаем строку таблицы
    for row in df.itertuples():
        # Контейнер для обработанных транскрипций
        new_transcriptions = []
        # Делаем из строки транскрипций полноценный список
        transcriptions = row.transcriptionRu.split(',')
        # Проходимся циклом по всем русских транскрипциям в строке
        for transcription in transcriptions:
            # Снятие пробелов и косых чер
            transcription = transcription.replace('/', '').replace('.', '').strip()
            # Осуществление замен
            for old, new in replacements.items():
                transcription = transcription.replace(old, new)
            # Принятие правок
            for pattern, replacement in remarks.items():
                transcription = re.sub(pattern, replacement, transcription)
            # Проверка на запрещенные символы
            for symbol in transcription:
                if symbol not in allowed_char:
                    # Переключаем флаг
                    flag = False
                    # Логгируем произведенные замены
                    print(transcription, '->', symbol)
            # Добавляем каждую новую транскрипцию в контейнер
            new_transcriptions.append(transcription)
        # Пересобираем список новых транскрипций рбратно в строку
        new_transcriptions = ', '.join(new_transcriptions)
        # Обновляем загруженный скриптом csv
        idx = row.Index  # кортеж напрямую изменять нельзя, получаем его индекс
        df.at[idx, 'transcriptionRu'] = new_transcriptions

    # Сохраняем новую таблицу с премененными заменами
    df.to_csv("output.csv", index=False, encoding='utf-8')
    # Если замен не было, уведомляем о правильности транскрипций
    if flag:
        print('No forbidden symbols detected. Operation completed successfully!')

# Вызов функции
substitute()