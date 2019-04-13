from flask import Flask
import sqlalchemy
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['CSRF_ENABLED'] = True
connection = sqlite3.connect('GymsNetwork.db', check_same_thread=False)
cursor = connection.cursor()

from app import routes