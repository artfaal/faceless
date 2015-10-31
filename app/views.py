from app import app, mongo
from flask import render_template


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/catalog/', methods=['GET'])
def catalog():
    category = mongo.test.category.find().sort('position')

    return render_template('catalog.html', category=category)
