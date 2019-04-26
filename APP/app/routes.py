from app import app, models
from flask import render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegAsClientForm
from app.models import CLIENT, COACH, ADMIN
import datetime

# Проверяет данные с формы авторизации (0 - если нет такого профиля, объект - если профиль есть)
def VerifyAuthData(form):
    login = request.form['username']
    password = request.form['password']
    role = request.form['roles']
    if (role == 'coach'):
        coach = COACH.select().where((COACH.Login == login) & (COACH.Password == password))
        if (coach):
            return coach
        else:
            return 0
    if (role == 'client'):
        client = CLIENT.select().where((CLIENT.Login == login) & (CLIENT.Password == password))
        if (client):
            return client
        else:
            return 0
    if (role == 'admin'):
        admin = ADMIN.select().where((ADMIN.Login == login) & (ADMIN.Password == password))
        if (admin):
            return admin
        else:
            return 0

# Проверяем данные с формы регистрации клиента
def VerifyRegClientData(form):
    fio = request.form['fio']
    login = request.form['username']
    password = request.form['password']
    birth = request.form['birth']
    level = request.form['level']

    client = CLIENT.create(Login = login,
                           Password = password,
                           BirthDate = birth,
                           SubLevel = int(level),
                           FIO = fio,
                           TrainingsCount = 0,
                           SubSrartDate = datetime.date.today().strftime("%m-%d-%Y"),
                           )
    if (client):
        return client
    else:
        return 0

# Создать массив пунктов меню для пользователя
def CreateMenu():
    func = []
    if session['role'] == 'coach':
        func = [('viewShedule', 'Просмотреть расписание тренеровок'),
                ('changePrice','Изменить стоимость тренировок'),
                ]
    elif session['role'] == 'client':
        func = [('recording','Запись на тренировку'),
                ]
    elif session['role'] == 'admin':
        func = [('monitorCard', 'Отследить состояние абонемента клиента'),
                ('getCoaches', 'Вывести список тренеров'),
                ]
    return func


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template(
            'index.html',
            user=session['username'],
            funcs=CreateMenu(),
        )
    else:
        return render_template(
            'index.html',
            user='',
        )

@app.errorhandler(404)
def not_found(error):
    return render_template(
        "404.html",
    ), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Проверяем открыта ли сессия
    if 'username' in session:
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # Проверяем данные с формы
        element = VerifyAuthData(form)
        if(not element):
            flash('Вы ввели неверные данные, попробуйте еще раз')
            return redirect(url_for('login'))
        else:
            session['username'] = element[0].Login
            session['FIO'] = element[0].FIO
            session['role'] = request.form['roles']
            flash('Вы успешно авторизовались в системе')
            return redirect(url_for('index'))
    return render_template(
        'login.html',
        form = form,
    )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' not in session:
        flash('Вы еще не успели зайти в систему')
        return redirect(url_for('index'))
    else:
        session.pop('username', None)
        session.pop('FIO', None)
        session.pop('role', None)
        flash('Вы успешно вышли из системы')
        return redirect(url_for('index'))

@app.route('/regasclient', methods=['GET', 'POST'])
def regasclient():
    if 'username' in session:
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))

    form = RegAsClientForm()

    if form.validate_on_submit():
        element = VerifyRegClientData(form)
        if(not element):
            flash('Вы ввели неверные данные, попробуйте еще раз')
            return redirect(url_for('index'))
        else:
            print("Клиент {} добавлен в БД".format(element.FIO))
            session['username'] = element.Login
            session['FIO'] = element.FIO
            session['role'] = 'client'
            flash('Вы успешно зарегистрировались в системе')
            return redirect(url_for('index'))

    return render_template(
        'regasclient.html',
        form = form
    )

@app.route('/viewShedule', methods=['GET', 'POST'])
def viewShedule():
    print("Успешно")

@app.route('/changePrice', methods=['GET', 'POST'])
def changePrice():
    print("Успешно")

@app.route('/recording', methods=['GET', 'POST'])
def recording():
    print("Успешно")

@app.route('/monitorCard', methods=['GET', 'POST'])
def monitorCard():
    print("Успешно")

@app.route('/getCoaches', methods=['GET', 'POST'])
def getCoaches():
    print("Успешно")