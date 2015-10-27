# -*- coding: utf-8 -*-
# import pymongo
import csv
import sys
# import re

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")


# Имя базы данных
DB_NAME = 'name_of_the_base'

# Предобработка csv файлов
FILENAME = 'pechi_small.csv'


def makedic():
    with open(FILENAME, 'rb') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        # mydict = {rows[ARTICLE]: onlynum(rows[PRICE]) for rows in reader}
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


if __name__ == '__main__':
    makedic()
