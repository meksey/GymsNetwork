from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
    username = StringField("Введите логин: ", validators=[DataRequired()])
    password = PasswordField("Введите пароль: ", validators=[DataRequired()])
    roles = RadioField("Выберите роль в системе: ", choices=[('client','Клиент'),('coach', 'Тренер'),('admin', 'Администратор')])
    submit = SubmitField('Войти')
