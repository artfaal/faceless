# -*- coding: utf-8 -*-
from app import app, utility
from utility.convert_xlsx_to_csv import run_convert
from models import DB


@app.route('/secret/<token>', methods=['GET'])
def secret(token):
    db = DB()
    cat = db.get_db('cat')
    items = db.get_db('items')
    pages = db.get_db('pages')

    if token == app.config['TOKEN_XLSX_TO_CSV']:
        run_convert()
        return 'Convert xlsx to csv files in folder \n'
    elif token == app.config['REMOVE_CATEGORY_COLLECTION']:
        cat.drop()
        return 'Remove all from "category" collection \n'
    elif token == app.config['REMOVE_ITEMS_COLLECTION']:
        items.drop()
        return 'Remove all from "items" collection \n'
    elif token == app.config['REMOVE_PAGES_COLLECTION']:
        pages.drop()
        return 'Remove all from "Pages" collection \n'
    elif token == app.config['WRITE_TO_CATEGORY']:
        utility.import_db.save_category_to_db()
        return 'Write in DB from "category" csv file \n'
    elif token == app.config['WRITE_TO_ITEMS']:
        utility.import_db.save_items_to_db()
        return 'Write in DB from "items" csv files \n'
    elif token == app.config['WRITE_TO_PAGES']:
        utility.import_db.save_pages_to_db()
        return 'Write in DB from "Pages" csv files \n'
    else:
        return 'your token - \'%s\' didn\'t pass' % token
