# -*- coding: utf-8 -*-
import csv
import sys
from app import mongo, app
from validators import *
import os

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")


def save_items_to_db():
    files = get_items_csv()
    for file in files:
        with open(os.path.join(app.config['TMP_PATH'], file), 'rb') as f:
            reader = csv.reader(f, dialect='excel', delimiter=';',
                                escapechar='\\')
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
    # Создаем, что бы упорядочить их по мере итерации.
    category_position = 10
    with open('%s%s' % (app.config['TMP_PATH'],
                        app.config['FILENAME_CATEGORY']), 'rb') as f:
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
                                                  'img':
                                                  pars_img_doc_video(row[6])
                                                  })
                    category_position += 10
                    add.save()


def save_pages_to_db():
    with open('%s%s' % (app.config['TMP_PATH'],
                        app.config['FILENAME_PAGES']), 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';',
                            escapechar='\\')
        for row in reader:
            if row[0][:1] != '^':  # Проверка на первую линию.
                add = mongo.Pages()
                add['section'] = row[0]
                add['name'] = row[1]
                add['slug'] = transliterate(row[1])
                add['body'] = row[2]
                add['meta_keywords'] = row[3]
                add['meta_description'] = row[4]
                add['mini_description'] = row[4]
                add['thumb'] = row[5]
                add['position'] = int_or_0(row[6])
                add.save()


def save_news_to_db():
    position = 0
    with open('%s%s' % (app.config['TMP_PATH'],
                        app.config['FILENAME_NEWS']), 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';',
                            escapechar='\\')
        for row in reader:
            if row[0][:1] != '^':  # Проверка на первую линию.
                add = mongo.News()
                add['name'] = row[0]
                add['slug'] = transliterate(row[0])
                add['position'] = position
                position += 1
                add['date'] = row[1]
                add['body'] = row[2]
                add['meta_keywords'] = row[3]
                add['meta_description'] = row[4]
                add.save()


def save_index_news_to_db():
    position = 0
    with open('%s%s' % (app.config['TMP_PATH'],
                        app.config['FILENAME_INDEX_NEWS']), 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';',
                            escapechar='\\')
        for row in reader:
            if row[0][:1] != '^':  # Проверка на первую линию.
                add = mongo.Index_News()
                add['name'] = row[0]
                add['img'] = row[1]
                add['link'] = row[2]
                add['mini_description'] = row[3]
                add['position'] = position
                position += 1
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
        try:
            result.append({'filename': part[0], 'alt': part[1],
                           'position': position})
            position += 1
        except IndexError:
            print '_' * 10, '\n', '\n Проблемы с этим выражением: \n', \
                  input, '\n'
    return result


def get_items_csv():
    #  Эта функция собирает все фалы из папки в список, кроме той,
    #  в которой лежат категории.
    list_of_files = []
    for file in os.listdir(app.config['TMP_PATH']):
        if file.endswith(".csv") and \
           file not in app.config['EXECUTE_FROM_ITEMS']:
            list_of_files.append(file)
    return list_of_files
