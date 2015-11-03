# -*- coding: utf-8 -*-
import csv
import sys
from app import mongo, app
from validators import *
import os

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")

# Предобработка csv файлов
# FILE_TO_IMPORT_ITEMS = app.config['FILE_TO_IMPORT_ITEMS']
FILE_TO_IMPORT_CATEGORY = app.config['FILE_TO_IMPORT_CATEGORY']
TMP_PATH = app.config['TMP_PATH']


def save_items_to_db():
    files = get_items_csv()
    for file in files:
        with open(os.path.join(TMP_PATH, file), 'rb') as f:
            reader = csv.reader(f, dialect='excel', delimiter=';', escapechar='\\')
            for row in reader:
                if row[0][:1] != '^':  # Проверка на первую линию.
                    add = mongo.Items()
                    add['name'] = row[0]
                    add['slug'] = transliterate(row[0])
                    add['main_category'] = row[1]
                    add['child_category'] = row[2]
                    add['body'] = row[3]
                    add['meta_keywords'] = row[4]
                    add['meta_description'] = row[5]
                    add['img'] = pars_img_doc_video(row[6])
                    add['video'] = pars_img_doc_video(row[7])
                    add['doc'] = pars_img_doc_video(row[8])
                    add['position'] = int_or_0(row[9])
                    add.save()


def save_category_to_db():
    """
    О Боги, я не знаю, как я справился с этой наркоманией.
    Суть в том, что в exel дочерние категории просто идут вслед за
    главными. Нужно было как-то дать понять, что если опять показывается главная
    категория, то надо записать закончившийся дочерний архив.
    Сначала ищет если в первой части данные. Если есть, значит это главная
    категория. Открывает класс Category который тянется из models.py.
    Пишутся все основные значение. Сохраняется. Следущее поле если
    оно дочерняя категория, уходит во вторую инерацию и пишутся в array.
    Точнее, мы просто append'им всё в один запрос и опять сохраняем.
    И так далее, пока опять не попадается родительная категория и там заново
    срабатывает класс Category, который обнуляет все значения и пишет по новой.
    """
    category_position = 10  # Создаем, что бы упорядочить их по мере итерации.
    with open(FILE_TO_IMPORT_CATEGORY, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';', escapechar='\\')
        for row in reader:
            # Проверяем главная ли это категория. Если - да,
            # перезаписываем её имя, как последнюю категорию.
            if row[0][:1] != '^':  # Проверка на первую линию.
                if row[0] != '':
                    # Самый важный параметр который обнуляет переменную,
                    # когда опять попадается родительская категория.
                    add = mongo.Category()
                    add['name'] = row[0]
                    add['slug'] = transliterate(row[0])
                    add['position'] = category_position
                    category_position += 10
                    if row[1] != '':
                        print 'Ошибка. В Родительской категории, кусок дочерней'
                        sys.exit(1)
                    add['mini_description'] = row[2]
                    add['body'] = row[3]
                    add['meta_keywords'] = row[4]
                    add['meta_description'] = row[5]
                    add['img'] = pars_img_doc_video(row[6])
                    add.save()
                elif row[1] != '':
                    add['child_category'].append({'name': row[1],
                                                  'slug': transliterate(row[1]),
                                                  'position': category_position,
                                                  'mini_description': row[2],
                                                  'body': row[3],
                                                  'meta_keywords': row[4],
                                                  'meta_description': row[5],
                                                  'img': pars_img_doc_video(row[6])
                                                  })
                    category_position += 10
                    add.save()


def pars_img_doc_video(input):
    # ex = "34_a.jpg$печь для сауны EOS 34 A&thermat.jpg$Для сауны EOS Thermat&"
    # Парсим участки с изображениями, видео и документами
    # Сначала разделяем основные части
    l = input.split('&')
    result = []
    position = 0  # Позиция картинок по порядку
    # Удаляем пустые значение
    if '' in l:
        l.remove('')
    # Создаем словарь и добавляем в итог
    for i in l:
        part = i.split('$')
        # Надо удалять первую строчку и CSV, иначе будет exception
        try:
            result.append({'filename': part[0], 'alt': part[1],
                           'position': position})
            position += 1
        except IndexError:
            print 'Error! Check first line in CSV file'
    return result


# def check_category():
#     # Вспомогательная функция, что бы визуально посмотреть,
#     # какие категории есть у товаров
#     with open(FILE_TO_IMPORT_ITEMS, 'rb') as f:
#         reader = csv.reader(f, dialect='excel', delimiter=';')
#         list_of_cat = []
#         count_of_items = 0
#         for row in reader:
#             count_of_items += 1
#             if row[1] not in list_of_cat:
#                 list_of_cat.append(row[1])

#             elif row[2] not in list_of_cat:
#                 list_of_cat.append(row[2])

#         for i in list_of_cat:
#             print i
#         print '=' * 40 + '\n Всего полей просканированно: %s' % count_of_items


def check_item_in_category():
    """
    Простая функция, которая проверяет все категории в items,
    на предмет их нахождения в коллекции категорий.
    Пробегается по всем категориям, включая дочерние.
    """
    # TODO переделать проверку под main и child
    raw_items = mongo.test.items.find()
    raw_category = mongo.test.category.find()
    list_of_cat_in_items = []
    list_of_all_category = []
    print '_'*40

    for i in raw_items:
        if i['category'] not in list_of_cat_in_items:
            list_of_cat_in_items.append(i['category'])
    for i in list_of_cat_in_items:
        print i
    print '_'*40

    for i in raw_category:
        if i['name'] not in list_of_all_category:
            list_of_all_category.append(i['name'])

        if i['child_category'] > 0:
            for b in i['child_category']:
                if b['name'] not in list_of_all_category:
                    list_of_all_category.append(b['name'])
    for i in list_of_all_category:
        print i
    print '_'*40
    for i in list_of_cat_in_items:
        if i not in list_of_all_category:
            print '%s not in category at all!' % i


def get_items_csv():
    list_of_files = []
    for file in os.listdir(TMP_PATH):
        if file.endswith(".csv") and not file.endswith("Category.csv"):
            list_of_files.append(file)
    return list_of_files
