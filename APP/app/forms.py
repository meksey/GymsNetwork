from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional
from app import models
import datetime


class LoginForm(FlaskForm):
    username = StringField("Введите логин: ", validators=[DataRequired()])
    password = PasswordField("Введите пароль: ", validators=[DataRequired()])
    roles = RadioField("Выберите роль в системе: ",
                       choices=[
                           ('client','Клиент'),
                           ('coach', 'Тренер'),
                           ('admin', 'Администратор')],
                       )
    submit = SubmitField('Войти')

def getlevels():
    levels = []
    for el in models.LEVELS.select():
        levels.append((str(el.ID), el.LevelName))
    return levels

class RegAsClientForm(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired()])
    birth = DateField("Дата рождения: ", format='%d-%m-%Y', validators=[Optional()], default=datetime.date.today())
    username = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    level = RadioField("Абонемент: ", choices=getlevels())
    submit = SubmitField("Регистрация")







