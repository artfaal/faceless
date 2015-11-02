# -*- coding: utf-8 -
from flask import Flask
from mongokit import Connection
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('config')
mongo = Connection()
Markdown(app)


from app import views, models, utility, evil
