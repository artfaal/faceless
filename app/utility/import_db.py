# -*- coding: utf-8 -*-
import csv
import sys
from app import mongo
from validators import *
from time import sleep
# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")
# Имя базы данных
DB_NAME = 'name_of_the_base'

# Предобработка csv файлов
FILENAME = 'tmp/category_s.csv'


def save_items_to_db():
    with open(FILENAME, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        for row in reader:
            add = mongo.test.items.Items()
            add['name'] = row[0]
            add['slug'] = transliterate(row[0])
            add['category'] = row[2]
            add['body'] = row[3]
            add['meta_keywords'] = row[4]
            add['meta_description'] = row[5]
            add['img'] = pars_img_doc_video(row[6])
            add['video'] = pars_img_doc_video(row[7])
            add['doc'] = pars_img_doc_video(row[8])
            add['position'] = int_or_0(row[9])
            add.save()


def save_category_to_db():
    with open(FILENAME, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        last_parent_cat = 0
        for row in reader:
            # Проверяем главная ли это категория. Если - да,
            # перезаписываем её имя, как последнюю категорию.
            if row[0] != '':
                add = mongo.test.category.Category()
                last_parent_cat = row[0]
                add['name'] = row[0]
                add['slug'] = transliterate(row[0])
                if row[1] != '':
                    print 'Ошибка. В Родительской категории, кусок дочерней'
                    sys.exit(1)
                add['mini_description'] = row[2]
                add['body'] = row[3]
                add['meta_keywords'] = row[4]
                add['meta_description'] = row[5]
                add['img'] = pars_img_doc_video(row[6])
                add.save()
        sys.exit()


def pars_img_doc_video(input):
    # ex = "34_a.jpg$печь для сауны EOS 34 A&thermat.jpg$Для сауны EOS Thermat&"
    # Парсим участки с изображениями, видео и документами
    # Сначала разделяем основные части
    l = input.split('&')
    result = []
    # Удаляем пустые значение
    if '' in l:
        l.remove('')
    # Создаем словарь и добавляем в итог
    for i in l:
        part = i.split('$')
        # Надо удалять первую строчку и CSV, иначе будет exception
        try:
            result.append({'filename': part[0], 'alt': part[1]})
        except IndexError:
            print 'Error! Check first line in CSV file'
    return result


def check_category():
    # Вспомогательная функция, что бы визуально посмотреть,
    # какие категории есть у товаров
    with open(FILENAME, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        list_of_cat = []
        count_of_items = 0
        for row in reader:
            count_of_items += 1
            if row[1] not in list_of_cat:
                list_of_cat.append(row[1])

            elif row[2] not in list_of_cat:
                list_of_cat.append(row[2])

        for i in list_of_cat:
            print i
        print '=' * 40 + '\n Всего полей просканированно: %s' % count_of_items
