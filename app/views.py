# -*- coding: utf-8 -*-
from app import app, mongo
from flask import render_template


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/catalog/', methods=['GET'])
@app.route('/catalog/<slug>', methods=['GET'])
def catalog(slug=None):
    category = mongo.test.category.find().sort('position')
    category2 = mongo.test.category.find().sort('position')
    category3 = mongo.test.category.find().sort('position')
    # Определяем, что эта страница будет посвящена этой категории.
    one_category = mongo.test.category.find_one({'slug': slug})
    if one_category:
        # Здесь находим все товары, которые из этой категории
        def items_from_category(child):
            """
            Из-за этой хрени я потратил порядка 3х часов.
            Jinja не хочет почему-то бегать до потери пульса по
            циклам for. Поэтому пришлось сократить этот цикл в шаблоне,
            заменив его на эту функцию. Аргумент - это имя той подкатегории,
            товары котрой надо отображать.
            """
            return mongo.test.items.find({'main_category':
                                          one_category['name'],
                                          'child_category': child})
        return render_template('catalog.html', category=category,
                               category2=category2, category3=category3,
                               slug=slug, one_category=one_category,
                               items_from_category=items_from_category)

    return render_template('catalog.html', category=category,
                           category2=category2, category3=category3,
                           slug=slug, one_category=one_category)
