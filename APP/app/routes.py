from app import app, models
from flask import render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegAsClientForm
from app.models import CLIENT, COACH, ADMIN

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
    birthdate = request.form['birthdate']
    sublevel = request.form['sublevel']

    client = CLIENT.create(Login = login,
                           Password = password,
                           BirthDate = birthdate,
                           Sub_ID = CLIENT.Client_ID,
                           SubLevel = int(sublevel),
                           FIO = fio,
                           TrainingsCount = 0,
                           )
    if (client):
        print("Охуенчик")
        return client
    else:
        print("Хуйня")
        return 0


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template(
            'index.html',
            user=session['username'],
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
            print(session['username'])
            print(session['FIO'] )
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
        flash('Вы успешно вышли из системы')
        return redirect(url_for('index'))


@app.route('/regasclient', methods=['GET', 'POST'])
def regasclient():
    form = RegAsClientForm()
    if form.validate_on_submit():
        print("Успех")
    return render_template(
        'regasclient.html',
        form = form
    )