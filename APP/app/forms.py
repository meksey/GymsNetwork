from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SelectMultipleField, PasswordField, SubmitField, RadioField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, InputRequired
from app import models
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime


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

class RegAsClientForm(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired()])
    username = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    submit = SubmitField("Регистрация")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegAsCoachForm(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired()])
    username = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    department = RadioField("Выберите свой филиал: ",
                            choices=models.DEPARTMENT.getDepList(),
                            )
    activity = MultiCheckboxField("Выберите какие типы дисциплин вы преподаете: ",
                           choices= models.ACTIVITY.getActivities(),
                           )
    submit = SubmitField("Регистрация")

# Добавляет выбранному пользователю тренировки
class AddSub(FlaskForm):
    login = StringField("Введите логин пользователя: ", validators=[DataRequired()])
    days = IntegerField("Введите количество занятий: ", validators=[DataRequired()], default=30)
    submit = SubmitField("Добавить абонемент")

# Посмотреть статус клиента и его абонемента админом
class ViewSub(FlaskForm):
    login = StringField("Введите логин пользователя: ", validators=[DataRequired()])
    submit = SubmitField("Посмотреть сведения о клиенте")

class RecordForm(FlaskForm):
    department = RadioField("Выберите фитнесс центр: ",
                            choices=models.DEPARTMENT.getDepList(),
                            )
    activity = RadioField("Выберите тип тренировки: ",
                          choices=models.ACTIVITY.getActivities(),
                          )
    start_time = DateTimeLocalField("Выберите желаемое время тренировки: ", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    submit = SubmitField("Выбрать тренера по заданным параметрам")

