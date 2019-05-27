from flask import Flask, Blueprint
from peewee import *
from flask_restplus import Api, Resource

app = Flask(__name__)

app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '3rfcewvreverrr'

blueprint = Blueprint('api', __name__)
api = Api(blueprint)
ns_client = api.namespace('clients', description='API клиента')
ns_coach = api.namespace('coachs', description='API тренера')
app.register_blueprint(blueprint, url_prefix='/api')

db = SqliteDatabase('GymsNetwork.db')

from app import models
from app import routes


