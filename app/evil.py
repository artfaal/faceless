# -*- coding: utf-8 -*-
from app import app, mongo, utility
from utility.convert_xlsx_to_csv import run_convert


@app.route('/secret/<token>', methods=['GET'])
def secret(token):
    if token == app.config['TOKEN_XLSX_TO_CSV']:
        run_convert()
        return 'Run command convert xlsx to csv files'
    elif token == app.config['REMOVE_CATEGORY_COLLECTION']:
        mongo.test.category.drop()
        return 'Drop CATEGORY collection'
    elif token == app.config['REMOVE_ITEMS_COLLECTION']:
        mongo.test.items.drop()
        return 'Drop ITEMS collection'
    elif token == app.config['WRITE_TO_CATEGORY']:
        utility.import_db.save_category_to_db()
        return 'Import Category from csv'
    elif token == app.config['WRITE_TO_ITEMS']:
        utility.import_db.save_items_to_db()
        return 'Import Category from csv'
    else:
        return 'your token - \'%s\' didn\'t pass' % token
