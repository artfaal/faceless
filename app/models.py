# -*- coding: utf-8 -*-
from mongokit import *
import datetime
from app import mongo, app
from utility.validators import *


@mongo.register
class Items(Document):
    """
    Документация по библиотеке
    https://github.com/namlook/mongokit/wiki
    """

    __database__ = app.config['DB']
    __collection__ = app.config['ITEM_COLLECTION']

    structure = {
        'name': basestring,
        'slug': basestring,
        'position': int,
        'meta_keywords': basestring,
        'meta_description': basestring,
        'body': basestring,
        'date_creation': datetime.datetime,
        # Сдесь сделал так, что у товара есть только одна категория.
        # Если нужно сделать так, что бы товар был в нескольких категориях
        # То нужно сделать это значение в виде листа. ex.: 'category': list
        'category': basestring,
        'img': [
            {
                'filename': basestring,
                'alt': basestring,
                'position': int
            }
        ],
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
    # TODO Индексы не работают, так что пока без них... -_-
    indexes = [
        {'fields': ['name'], 'unique': True},
        {'fields': ['slug'], 'unique': True},
        {'fields': ['body']},
    ]

    required_fields = []
    default_values = {
        'date_creation': datetime.datetime.utcnow,
        'position': 0
    }

    # TODO Странная ошибка с валидацией. Нужен юникод?
    validators = {
        # 'meta_keywords': max_length(200),
        # 'meta_description': max_length(200)
    }


@mongo.register
class Category(Document):

    __database__ = app.config['DB']
    __collection__ = app.config['CATEGORY_COLLECTION']

    structure = {
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
        ],

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

    indexes = [
        # TODO Плюс нужно сделать сделать индексы итерабельными
        # {'fields': ['name'], 'unique': True},
        # {'fields': ['child_category.name'], 'unique': True},
        # {'fields': ['slug'], 'unique': True},
        # {'fields': ['body']},

        # {'fields': ['child_category.name'], 'unique': True},
        # {'fields': ['child_category.slug'], 'unique': True},
        # {'fields': ['child_category.body']},
    ]

    required_fields = []

    default_values = {}

    validators = {
        # 'meta_keywords': max_length(200),
        # 'meta_description': max_length(200)
    }
