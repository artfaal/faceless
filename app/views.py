# -*- coding: utf-8 -*-
from app import app
from flask import render_template
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

    def category():
        return cat.find().sort('position')
    # Определяем, что эта страница будет посвящена этой категории.
    category_page = cat.find_one({'slug': category_slug})
    print category_page
    item_page = items.find_one({'slug': item_slug})

    if item_page:
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               item_page=item_page)

    elif category_page:
        # Здесь находим все товары, которые из этой категории
        def items_from_category(child):
            """
            Из-за этой хрени я потратил порядка 3х часов.
            Jinja не хочет почему-то бегать до потери пульса по
            циклам for. Поэтому пришлось сократить этот цикл в шаблоне,
            заменив его на эту функцию. Аргумент - это имя той подкатегории,
            товары котрой надо отображать.
            """
            return items.find({'main_category': category_page['name'],
                               'child_category': child})
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               items_from_category=items_from_category)
    else:
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page)
