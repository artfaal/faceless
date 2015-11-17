# -*- coding: utf-8 -
from flask import Flask
from mongokit import Connection
from flaskext.markdown import Markdown
from flask.ext.thumbnails import Thumbnail

app = Flask(__name__)
app.config.from_object('config')
mongo = Connection()
thumb = Thumbnail(app)
Markdown(app)

from app import views, models, utility, evil, forms
