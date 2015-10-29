# -*- coding: utf-8 -*-
import csv
import sys
from app import mongo
from validators import *

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")

# Имя базы данных
DB_NAME = 'name_of_the_base'

# Предобработка csv файлов
FILENAME = 'tmp/pechi.csv'


def makedic():
    with open(FILENAME, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        add = mongo.test.example.Items()
        for row in reader:
            # print 'Имя: %s' % row[0]
            # print 'Категории: %s | %s' % (row[1], row[2])
            # print 'Описание: %s...' % row[3][:100]
            # print 'Ключевики (SEO): %s...' % (row[4][:100])
            # print 'Мета-Описание (SEO): %s...' % (row[5][:100])
            # print 'Картинки: %s' % (row[6][:50])
            # print 'Видео: %s' % (row[7][:100])
            # print 'Инструкции: %s' % (row[8][:100])
            # print 'Позиция: %s' % (row[9][:100])
            # print 'Так же покупают: %s' % (row[10][:100])
            # print '='*50
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


#
def check_category():
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


def save_to_db():
    # Сохраняем всё в базу
    add = mongo.test.example.Items()
    add['name'] = 'testing'
    print add
