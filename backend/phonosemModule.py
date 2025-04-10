import sqlite3
from customFunctions.misc import *
from customFunctions.moulds import *
import spacy
import re
import pymorphy3

def phonosemTool(request: str) -> list:
    """
    That is a function that performs phonosemantic calculations when picking more relevant and iconic translations
    """
    # Перебираем файлы в директории
    paths = pathfinder(dirname='materials')
    database = paths["database"]
    if not database:
        data = [{
            "verb" : "Датабаза не обнаружена",
            "category" : "",
            "meaning" : "",
            "transcription" : "",
            "transitivity" : "",
            "translations" : "",
            "scores" : "",
            "transitivities" : ""
        }]
        return data

    # NLQ сегмент spaCy
    nlp = spacy.load("en_core_web_trf")  # тяжеловесная CPU модель для английского языка
    tokens, verbs, results, verb_flag = nlp(request), [], [], False
    # Находим глаголы
    for token in tokens:
        # Лемматизируем
        if token.pos_ == 'VERB':
            verb_flag = True
            verbs.append(token.lemma_)
            # Определение переходности английских глаголов в предложении
            transitivityEn = ''
            # Пропускаем, если инпут имеет to и короче 3, не имеет to и короче 2
            if ('to' in [str(x) for x in tokens] and len(tokens) > 2) or ('to' not in [str(x) for x in tokens] and len(tokens) > 1):
                indirect_object = False
                direct_object = False
                for item in token.children:
                    if(item.dep_ == "iobj" or item.dep_ == "pobj"):
                        indirect_object = True
                    if (item.dep_ == "dobj" or item.dep_ == "dative"):
                        direct_object = True
                if indirect_object and direct_object:
                    transitivityEn = 'переходный'
                elif direct_object and not indirect_object:
                    transitivityEn = 'переходный'
                elif not direct_object and not indirect_object:
                    transitivityEn = 'непереходный'
                else:
                    transitivityEn = ''
    # Учет низкочастотных глаголов
    if verb_flag == False and len(tokens) == 2 and tokens[0].text == 'to' and tokens[1].text != 'to' and tokens[1].text.isalpha():
        verbs.append(tokens[1].lemma_)
        verb_flag, transitivityEn = True, ''
    # Обработка исключений
    if verb_flag != True:
        data = [{
            "verb" : "В вашем запросе нет глагола",
            "category" : "",
            "meaning" : "",
            "transcription" : "",
            "transitivity" : "",
            "translations" : "",
            "scores" : "",
            "transitivities" : ""
        }]
        return data

    # Устанавливаем соединение с датабазой
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row   # Возвращаем словарь
    cursor = conn.cursor()
    # Достаем информацию из датабазы
    for verb in verbs:
        cursor.execute("""
            SELECT verbs.verb, verbs.transcription, verbs.category, verbs.meaning,
                GROUP_CONCAT(translations.word, ', ') AS translations,
                GROUP_CONCAT(translations.transcription, ', ') AS transcriptionsRu
            FROM verbs
            JOIN translations ON verbs.id = translations.parentId
            WHERE verbs.verb = ?
            GROUP BY verbs.id;
        """, (verb,))
        result = cursor.fetchone()
        if result:
            results.append(dict(result))  # Если глагол есть в датабазе
    # Проверки на вхождение в ДБ
    if not results:
        data = [{
            "verb" : "Введенный глагол не является глаголом движения",
            "category" : "",
            "meaning" : "",
            "transcription" : "",
            "transitivity" : "",
            "translations" : "",
            "scores" : "",
            "transitivities" : ""
        }]
        conn.close()
        return data
    conn.close()
    
    # Обработка полученных из ДБ глаголов и информации о них
    total_verb_info = []
    for result in results:
        # Парсинг строк в списки
        result['translations'] = [verb.strip() for verb in result['translations'].split(',')]
        result['transcriptionsRu'] = [verb.strip() for verb in result['transcriptionsRu'].split(',')]
        # Сортировка результатов
        category, penalty, sorted_verbs, transcriptionEn, meaning, verb = result['category'], 0.8, [], result['transcription'], result['meaning'], result['verb']
        translations, scores, transitivities = [], [], []
        cat_info = ""
        for transcription, translation in zip(result['transcriptionsRu'], result['translations']):
            # Определение переходности русских эквивалентов
            transitivityRu = ''
            # Определяем, если найдена английская транзитивность
            if transitivityEn:
                morph = pymorphy3.MorphAnalyzer()
                # Вырезаем слова в круглых скобках
                cut = re.sub(r'\(.*\)', '', translation).strip()
                p = morph.parse(cut)
                for x in p:
                    if x.tag.POS == 'INFN':
                        if x.tag.transitivity == 'tran':
                            transitivityRu = 'переходный'
                        else:
                            transitivityRu = 'непереходный'
                        break
                    else:
                        transitivityRu = ''
            # Обработка русской транскрипции регулряным выражением, отсечение суффиксов инфинитива
            transcription = transcription.replace('’', '')
            pattern = r"(at|et|it|ыt|ыvat|ivat|avat|nut|aca|eca|ica|ыvaca|ivaca|avaca|nuca|ti|ca|t)$"
            transcription = re.sub(pattern, '', transcription)
            # Вырезаем элементы в круглых скобках
            # transcription = re.sub(r'\(.*\)', '', translation).strip()
            print('NB', transcription)
            best_score = 0
            # Обработка нефоносемантических глаголов движения
            if category == '-':
                cat_info = "нет фоносемантического значения"
            # Обработка ЗС
            elif category in [
                'SHM', 'CLC', 'CHW', 'SCK', 'BIT', 'SPT', 'GLP', 'CHK', 'LCK', 'VMT', 'SMC', 'SLM'
            ]:
                cat_info = 'звукосимволизм'
                # Проверка на наличие важных фонотипов
                for phonotype in symbolTemplates[category]:
                    count = transcription.count(phonotype)
                    best_score += count
            # Обработка ЗП
            else:
                cat_info = 'звукоподражание'
                # Переводим транскрипцию в набор фонотипов
                combination = ''  # Результат
                for phoneme in transcription:
                    for key in phonotypes:
                        if phoneme in phonotypes[key]:
                            combination += key
                # Проходим по всем шаблонам одной категории
                for template in onomTemplates[category]:
                    # Проходим по всем вариациям шаблона
                    for blueprint in template['blueprint']:
                        # Считаем расстояние по отношению к каждому шаблону
                        score = fuzz.partial_ratio(blueprint, combination)  # Частичное сравнение по первому вхождению
                        # Проверяем, включает ли набор наиболее важные фонотипы
                        if template['essentials']:
                            essential_flag = False
                            for essential in template['essentials']:
                                # if essential in combination:
                                if re.search(essential, combination):
                                    # print(re.match(essential, combination))
                                    essential_flag = True
                            # Награждаем, если включают
                            if essential_flag:
                                if template['penalty']:
                                    # Уникальная награда
                                    score += (1 - template['penalty']) * score
                                else:
                                    # Стандартная награда
                                    score += (1 - penalty) * score
                            # Накладываем штраф, если не включают
                            if not essential_flag:
                                if template['penalty']:
                                    # Уникальный штраф
                                    score *= template['penalty']
                                else:
                                    # Стандартный штраф
                                    score *= penalty
                        # Находим наиболее высокий счет
                        if score > best_score:
                            best_score, best_blueprint = int(score), blueprint
                        
            # Запись результата
            translations.append(translation)
            scores.append(best_score)
            transitivities.append(transitivityRu)
        # сортировка
        combined = list(zip(translations, scores, transitivities))
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
        sorted_translations, sorted_scores, sorted_transitivities = zip(*sorted_combined)
        sorted_translations, sorted_scores, sorted_transitivities = list(sorted_translations), list(sorted_scores), list(sorted_transitivities)
        data = {
            "verb" : verb,
            "category" : cat_info,
            "meaning" : meaning,
            "transcription" : transcriptionEn,
            "transitivity" : transitivityEn,
            "translations" : sorted_translations,
            "scores" : sorted_scores,
            "transitivities" : sorted_transitivities
        }
        total_verb_info.append(data)

    return total_verb_info