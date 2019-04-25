from flask import Flask
from peewee import *



app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '3rfcewvreverrr'


db = SqliteDatabase('GymsNetwork.db')

from app import models
from app import routes


def WriteClients():
    print("Клиенты: ")
    for client in models.CLIENT.select():
        print(client.FIO)

def WriteCoaches():
    print("Тренера: ")
    for coach in models.COACH.select():
        print("Тренер {} работает в филиале гопода {} ".format(coach.FIO, models.DEPARTMENT.get(models.DEPARTMENT.Dep_ID == coach.Dep_ID).City))


def WriteDeps():
    print("Филиалы: ")
    for dep in models.DEPARTMENT.select():
        print(dep.Dep_ID, dep.City)

def test():
    levels = []
    for element in models.LEVELS.select():
        levels.append((str(element.Level), element.LevelName))
    print(levels)
