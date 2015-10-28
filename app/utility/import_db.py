# -*- coding: utf-8 -*-
import csv
import sys
from app import mongo

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
        for row in reader:
            print 'Имя: %s' % (row[0])
            print 'Категории: %s | %s' % (row[1], row[2])
            print 'Описание: %s...' % row[3][:100]
            print 'Ключевики (SEO): %s...' % (row[4][:100])
            print 'Мета-Описание (SEO): %s...' % (row[5][:100])
            print 'Картинки: %s' % (row[6][:50])
            print 'Видео: %s' % (row[7][:100])
            print 'Инструкции: %s' % (row[8][:100])
            print 'Позиция: %s' % (row[9][:100])
            print 'Так же покупают: %s' % (row[10][:100])
            print '='*50


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


def save_to_db():
    add = mongo.test.example.Items()
    add['name'] = 'testing'
    print add
