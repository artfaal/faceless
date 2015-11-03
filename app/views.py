# -*- coding: utf-8 -*-
from app import app
from flask import render_template, send_from_directory
from models import DB


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/catalog/', methods=['GET'])
@app.route('/catalog/<category_slug>', methods=['GET'])
@app.route('/catalog/<category_slug>/<item_slug>', methods=['GET'])
def catalog(category_slug=None, item_slug=None):
    db = DB()
    cat = db.get_db('cat')
    items = db.get_db('items')

    #  Функия для вомзможности множественного вызова внутри страницы.
    def category():
        return cat.find().sort('position')

    #  Получаем значения
    item_page = items.find_one({'slug': item_slug})
    category_page = cat.find_one({'slug': category_slug})

    # Страница продукта?
    if item_page:
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               item_page=item_page)
    #  Страница категории?
    elif category_page:
        def items_from_child_category(child):
            return items.find({'main_category': category_page['name'],
                               'child_category': child})

        def items_from_main_category():
            return items.find({'main_category': category_page['name']})

        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               items_from_child_category=items_from_child_category,
                               items_from_main_category=items_from_main_category)
    #  Значит catalog/
    else:
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page)


@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/cache/<path:filename>')
def cache(filename):
    return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)
