from flask import Flask
from peewee import *



app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '3rfcewvreverrr'


db = SqliteDatabase('GymsNetwork.db')

from app import models
from app import routes
