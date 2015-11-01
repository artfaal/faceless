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
    name_of_category = mongo.test.category.find_one({'slug': slug})

    return render_template('catalog.html', category=category,
                           category2=category2, category3=category3, slug=slug, name_of_category=name_of_category)

