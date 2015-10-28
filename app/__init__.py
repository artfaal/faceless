# -*- coding: utf-8 -
from flask import Flask
from mongokit import Connection

app = Flask(__name__)
app.config.from_object('config')
mongo = Connection()


from app import views, models, utility

utility.import_db.pars_img_doc_video()
