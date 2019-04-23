from flask import Flask
from peewee import *



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['CSRF_ENABLED'] = True

db = SqliteDatabase('GymsNetwork.db')

from app import models
from app import routes

for res in models.WORK_DAY.select():
    print(res.Weekday_title)
