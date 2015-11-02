# -*- coding: utf-8 -*-
from app import app, utility
from utility.convert_xlsx_to_csv import run_convert
from models import DB


@app.route('/secret/<token>', methods=['GET'])
def secret(token):
    db = DB()
    cat = db.get_db('cat')
    items = db.get_db('items')

    if token == app.config['TOKEN_XLSX_TO_CSV']:
        run_convert()
        return 'Run command convert xlsx to csv files'
    elif token == app.config['REMOVE_CATEGORY_COLLECTION']:
        cat.drop()
        return 'Drop CATEGORY collection'
    elif token == app.config['REMOVE_ITEMS_COLLECTION']:
        items.drop()
        return 'Drop ITEMS collection'
    elif token == app.config['WRITE_TO_CATEGORY']:
        utility.import_db.save_category_to_db()
        return 'Import Category from csv'
    elif token == app.config['WRITE_TO_ITEMS']:
        utility.import_db.save_items_to_db()
        return 'Import Category from csv'
    else:
        return 'your token - \'%s\' didn\'t pass' % token
