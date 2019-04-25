from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, regexp
from app import models


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
        levels.append((str(el.Level), el.LevelName))
    return levels

class RegAsClientForm(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired()])
    birth = StringField("Дата рождения: ", validators=[DataRequired()])
    username = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    level = RadioField("Абонемент: ", choices=getlevels())
    submit = SubmitField("Регистрация")







