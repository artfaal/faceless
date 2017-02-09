# -*- coding: utf-8 -
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from mongokit import Connection
from flaskext.markdown import Markdown
from flask.ext.thumbnails import Thumbnail
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail
from flask_recaptcha import ReCaptcha

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
mongo = Connection()
thumb = Thumbnail(app)
assets = Environment(app)
Markdown(app, extensions=['attr_list'])
mail = Mail(app)
CsrfProtect(app)
recaptcha = ReCaptcha(app=app)

js = Bundle('assets/vendor/jQuery/jquery-1.11.3.min.js',
            'assets/vendor/jQueryUI/jquery-ui.min.js',
            'assets/vendor/holder-js/holder.js',
            'assets/vendor/lightbox/js/lightbox.js',
            'assets/vendor/scroll_top/scroll.js',
            'assets/vendor/js.cookie/js.cookie.js',
            'assets/vendor/slick/slick.min.js',
            'assets/vendor/match-height/match-height-min.js',
            'assets/js/main.js',
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

css = Bundle('assets/vendor/skeleton/skeleton.css',
             'assets/vendor/skeleton/normalize.css',
             'assets/vendor/lightbox/css/lightbox.css',
             'assets/vendor/font-awesome/css/font-awesome.css',
             'assets/vendor/scroll_top/style.css',
             'assets/vendor/slick/slick.css',
             'assets/vendor/slick/slick-theme.css',

             filters='cssmin', output='gen/packed.css')
assets.register('css_all', css)

scss = Bundle('assets/scss/*',
              filters='pyscss', output='gen/packed_scss.css')
assets.register('scss_all', scss)

from app import views, models, utility, auth, evil, forms
