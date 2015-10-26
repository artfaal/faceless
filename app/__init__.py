from flask import Flask
from mongokit import Connection

app = Flask(__name__)
app.config.from_object('config')
connection = Connection()


from app import views, models

