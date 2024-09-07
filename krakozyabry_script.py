"""Перевод с эльфийского. Транслитерация букв. Скрипт по обработке текста"""

eng_1 = ["`qwertyuiop[]asdfghjkl;'\zxcvbnm,./"]
rus_1 = ["ёйцукенгшщзхъфывапролджэ\ячсмитьбю."]
eng_2 = ['~@#$^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?']
rus_2 = ['Ё"№;:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,']

eng_1_lst = []  # Добавим буквы в списки как отдельные элементы
for i in eng_1:
    eng_1_lst += i
rus_1_lst = []
for i in rus_1:
    rus_1_lst += i
eng_2_lst = []
for i in eng_2:
    eng_2_lst += i
rus_2_lst = []
for i in rus_2:
    rus_2_lst += i


def match_rus(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    """Проверим строку на русские буквы: True/False"""
    return not alphabet.isdisjoint(text.lower())


def match_eng(text, alphabet=set('abcdefghijklmnopqrstuvwxyz')):
    """Проверим строку на английские буквы: True/False"""
    return not alphabet.isdisjoint(text.lower())


def translation(text):
    """Произведём транслитерацию букв и символов"""
    global eng_1_lst, rus_1_lst, eng_2_lst, rus_2_lst, text_after
    text_after = ''
    for let in text:
        if let in rus_1_lst and match_rus(text) is True:
            ind = rus_1_lst.index(let)
            text_after += eng_1_lst[ind]
        elif let in rus_2_lst and match_rus(text) is True:
            ind = rus_2_lst.index(let)
            text_after += eng_2_lst[ind]
        elif let in eng_1_lst and match_eng(text) is True:
            ind = eng_1_lst.index(let)
            text_after += rus_1_lst[ind]
        elif let in eng_2_lst and match_eng(text) is True:
            ind = eng_2_lst.index(let)
            text_after += rus_2_lst[ind]
        else:
            text_after += let
    return text_after
