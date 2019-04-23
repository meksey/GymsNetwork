from flask import Flask
from peewee import *



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['CSRF_ENABLED'] = True

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




WriteClients()
WriteCoaches()
WriteDeps()
