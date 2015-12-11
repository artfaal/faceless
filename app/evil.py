# -*- coding: utf-8 -*-
from app import app, utility
from utility.convert_xlsx_to_csv import run_convert
from models import DB


@app.route('/secret/<token>', methods=['GET'])
def secret(token):
    db = DB()
    cat = db.get_db('category')
    items = db.get_db('items')
    pages = db.get_db('pages')
    news = db.get_db('news')
    i_news = db.get_db('index_news')
    i_slider = db.get_db('index_slider')

    if token == app.config['FULL_RM_WRITE']:
        run_convert()
        cat.drop()
        items.drop()
        pages.drop()
        news.drop()
        i_news.drop()
        i_slider.drop()
        utility.import_db.save_category_to_db()
        utility.import_db.save_items_to_db()
        utility.import_db.save_pages_to_db()
        utility.import_db.save_news_to_db()
        utility.import_db.save_index_news_to_db()
        utility.import_db.save_index_slider_to_db()
        return 'Full RM/WRITE BASE \n'
    else:
        return 'your token - \'%s\' didn\'t pass' % token
