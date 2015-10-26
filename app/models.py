from mongokit import Document
import datetime


class Item(Document):
    structure = {
        'name': basestring,
        'slug': basestring,
        'position': int,
        'meta_keywords': basestring,
        'meta_description': basestring,
        'body': basestring,
        'date_creation': datetime.datetime,
        'img': [
            {
                'filename': basestring,
                'alt': basestring,
            }
        ],
        'doc': [
            {
                'filename': basestring,
                'alt': basestring,
            }
        ],
        'video': [
            {
                'url': basestring,
                'alt': basestring,
            }
        ]
    }
    required_fields = []
    default_values = {
        'date_creation': datetime.datetime.utcnow
    }
    validators = {
    }


class Category(Document):
    structure = {
        'name': basestring,
        'slug': basestring,
        'position': int,
        'meta_keywords': basestring,
        'meta_description': basestring,
        'mini_description': basestring,
        'body': basestring,
        'date_creation': datetime.datetime,
        'img': [
            {
                'filename': basestring,
                'alt': basestring,
            }
        ],
        'child_category': {
            'name': basestring,
            'slug': basestring,
            'position': int,
            'meta_keywords': basestring,
            'meta_description': basestring,
            'mini_description': basestring,
            'body': basestring,
            'date_creation': datetime.datetime,
            'img': [
                {
                    'filename': basestring,
                    'alt': basestring,
                }
            ]
        }
    }
    required_fields = []
    default_values = {
        'date_creation': datetime.datetime.utcnow
    }
    validators = {
    }
