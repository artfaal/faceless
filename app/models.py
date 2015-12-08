# -*- coding: utf-8 -*-
from mongokit import *
import datetime
from app import mongo, app
from utility.validators import *
from random import choice as choice
from app import mail
from flask.ext.mail import Message


class DB:
    """Класс для получения данных их БД"""
    def __init__(self):
        self.db = mongo[app.config['DB']]

    def get_db(self, param):
        return getattr(self.db, param)

    def get_all_img(self):
        f = self.get_db('items').find()
        img_filenames = []
        for i in f:
            for img in i['img']:
                try:
                    img_filenames.append(img['filename'])
                except Exception as e:
                    print 'Maybe no img in: ', i['name'], e
        return img_filenames


class _Base(Document):
    """
    Документация по библиотеке
    https://github.com/namlook/mongokit/wiki
    Базовый класс для создания элементов в базе
    """
    __database__ = app.config['DB']

    structure = {
        'name': basestring,
        'slug': basestring,
        'position': int,
        'meta_keywords': basestring,
        'meta_description': basestring,
        'body': basestring,
        'img': [
            {
                'filename': basestring,
                'alt': basestring,
                'position': int
            }
        ]
    }


@mongo.register
class Items(_Base):
    """Товары"""
    __collection__ = app.config['ITEM_COLLECTION']

    structure = {
        'date_creation': datetime.datetime,
        'main_category': basestring,
        'child_category': basestring,
        'doc': [
            {
                'filename': basestring,
                'alt': basestring,
                'position': int
            }
        ],
        'video': [
            {
                'filename': basestring,
                'alt': basestring,
                'position': int
            }
        ]
    }

    default_values = {
        'date_creation': datetime.datetime.utcnow,
        'position': 0
    }


@mongo.register
class Category(_Base):
    """Категории"""
    __collection__ = app.config['CATEGORY_COLLECTION']

    structure = {
        'mini_description': basestring,
        'child_category': [
            {
                'name': basestring,
                'slug': basestring,
                'position': int,
                'meta_keywords': basestring,
                'meta_description': basestring,
                'mini_description': basestring,
                'body': basestring,
                # 'date_creation': datetime.datetime,
                'img': [
                    {
                        'filename': basestring,
                        'alt': basestring,
                        'position': int
                    }
                ]
            }
        ],
    }


@mongo.register
class Pages(_Base):
    """Страницы"""
    __collection__ = app.config['PAGES_COLLECTION']

    structure = {
        'mini_description': basestring,
        'date_creation': datetime.datetime,
        'section': basestring,
        'thumb': basestring,
    }
    default_values = {
        'date_creation': datetime.datetime.utcnow,
        'position': 0
    }


@mongo.register
class News(_Base):
    """Новости/Блог"""
    __collection__ = app.config['NEWS_COLLECTION']

    structure = {
        'date': basestring,
    }


def bg_for_index():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(app.config['BG_INDEX'])
                 if isfile(join(app.config['BG_INDEX'], f))]
    return str(choice(onlyfiles))


class MailSend:
    """Mail"""
    def __init__(self):
        self.sender = app.config['MAIL_SENDER']
        self.recepients = app.config['MAIL_RECEPIENTS']
        self.title_feedback = app.config['MAIL_FEEDBACK_TITLE']
        self.body_feedback = app.config['MAIL_FEEDBACK_BODY']
        self.title_service_query = app.config['MAIL_SERVICE_QUERY_TITLE']
        self.body_service_query = app.config['MAIL_SERVICE_QUERY_BODY']

    def send_feedback(self, url_from, name, email=None, phone=None, body=None):
        msg = Message(
            self.title_feedback % name,
            sender=self.sender,
            recipients=self.recepients)
        msg.html = self.body_feedback % (name, url_from, email, phone, body)
        mail.send(msg)

    def send_service_query(self, equipment, name, email=None,
                           phone=None, body=None, comment=None):
        msg = Message(
            self.title_service_query % name,
            sender=self.sender,
            recipients=self.recepients)
        msg.html = self.body_service_query % (equipment, name, email,
                                              phone, body, comment)
        mail.send(msg)
