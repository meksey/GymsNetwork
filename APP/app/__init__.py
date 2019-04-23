from flask import Flask

from flask_peewee.db import Database

DATABASE = {
    'name': 'GymsNetwork.db',
    'engine': 'peewee.SqliteDatabase',
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['CSRF_ENABLED'] = True

db = Database(app)

from app import routes
