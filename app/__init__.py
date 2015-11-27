# -*- coding: utf-8 -
from flask import Flask
from mongokit import Connection
from flaskext.markdown import Markdown
from flask.ext.thumbnails import Thumbnail
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')
mongo = Connection()
thumb = Thumbnail(app)
assets = Environment(app)
Markdown(app)
mail = Mail(app)

js = Bundle('assets/vendor/jQuery/jquery-1.11.3.min.js',
            'assets/vendor/holder-js/holder.js',
            'assets/vendor/lightbox/js/lightbox.js',
            'assets/vendor/basic-jquery-slider/js/bjqs-1.3.min.js',
            'assets/js/main.js',
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

css = Bundle('assets/vendor/skeleton/normalize.css',
             'assets/vendor/skeleton/skeleton.css',
             'assets/vendor/basic-jquery-slider/bjqs.css',
             'assets/vendor/lightbox/css/lightbox.css',
             'assets/vendor/font-awesome/css/font-awesome.css',
             'assets/css/main.css',
             filters='cssmin', output='gen/packed.css')
assets.register('css_all', css)

from app import views, models, utility, evil, forms
