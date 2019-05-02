from app import app, models
from flask import render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegAsClientForm, RegAsCoachForm, AddSub, ViewSub
from app.models import CLIENT, SUBSCRIPTION, COACH, ADMIN, DEPARTMENT, COACH_ACTIVITY


# Добавить тренера (0 если не удалось)
def addCoach(fio, login, password, dep, acts):
    flag = False
    try:
        COACH.get(COACH.Login == login)
    except:
        flag = True
    if flag:
        COACH.insert(FIO = fio,
                     Login = login,
                     Password = password,
                     Dep = dep).execute()
        coach = COACH.get(COACH.Login == login)
        for act in acts:
            COACH_ACTIVITY.insert(Coach_ID = coach.ID, Activity_ID = act).execute()
        return coach
    else:
        return 0

# Добавить клиента
def addClient(fio, login, password):
    flag = False
    try:
        CLIENT.get(CLIENT.Login == login)
    except:
        flag = True
    if flag:
        CLIENT.insert(FIO = fio,
                      Login = login,
                      Password = password,
                      ).execute()
        client = CLIENT.get(CLIENT.Login == login)
        return client
    else:
        return 0

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

# Проверяет возможно ли добавление абонемента, если да, то возвращает объект клиента
def CheckAddCart(login, days):
    if (days <= 0) or (days >500):
        flash('Введено недопустимое количество дней')
        return 0
    try:
        CLIENT.get(CLIENT.Login == login)
    except:
        flash('Такого пользователя не существует')
        return 0
    client = CLIENT.get(CLIENT.Login == login)
    return client

# Создать массив пунктов меню для пользователя
def CreateMenu():
    func = []
    if session['role'] == 'coach':
        func = [('viewShedule', 'Просмотреть расписание тренеровок'),
                ]
    elif session['role'] == 'client':
        func = [('recording','Запись на тренировку'),
                ]
    elif session['role'] == 'admin':
        func = [('addSub', 'Добавить тренировки клиенту'),
                ('viewSub', 'Проверить статус абонемента')
                ]
    return func


"""
            ______Маршруты______
"""

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
            if request.form['roles'] != 'admin':
                session['FIO'] = element[0].FIO
            else:
                session['FIO'] = 'Администратор'
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
        element = addClient(request.form['fio'], request.form['username'], request.form['password'])
        if(not element):
            flash('Пользователь с таким логином уже существует')
            return redirect(url_for('index'))
        else:
            session['username'] = element.Login
            session['FIO'] = element.FIO
            session['role'] = 'client'
            flash('Вы успешно зарегистрировались в системе')
            return redirect(url_for('index'))
    return render_template(
        'regasclient.html',
        form = form,
    )

@app.route('/regascoach', methods=['GET', 'POST'])
def regascoach():
    if 'username' in session:
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))
    form = RegAsCoachForm()
    if form.validate_on_submit():
        element = addCoach(request.form['fio'], request.form['username'], request.form['password'], form.department.data, form.activity.data)
        if(element == 0):
            flash('Пользователь с таким логином уже существует')
            return redirect(url_for('index'))
        else:
            session['username'] = element.Login
            session['FIO'] = element.FIO
            session['role'] = 'coach'
            flash('Вы успешно зарегистрировались в системе')
            return redirect(url_for('index'))
    return render_template(
        'regascoach.html',
        form=form,
    )



@app.route('/viewShedule', methods=['GET', 'POST'])
def viewShedule():
    print("Успешно")

@app.route('/recording', methods=['GET', 'POST'])
def recording():
    print("Успешно")

@app.route('/addSub', methods=['GET', 'POST'])
def addSub():
    if session['role'] != 'admin':
        flash('У вас недостаточно прав для совершения данной операции')
        return redirect(url_for('index'))
    form = AddSub()
    if form.validate_on_submit():
        login = request.form['login']
        days = request.form['days']
        client = CheckAddCart(login, int(days))
        if not client:
            return redirect(url_for('index'))
        if (ADMIN.addSub(client, int(days))):
            flash('Информация успешно обновлена')
            return redirect(url_for('index'))
    return render_template(
        'addSub.html',
        form=form,
        funcs=CreateMenu(),
    )

@app.route('/viewSub', methods=['GET', 'POST'])
def viewSub():
    if session['role'] != 'admin':
        flash('У вас недостаточно прав для совершения данной операции')
        return redirect(url_for('index'))
    form = ViewSub()
    if form.validate_on_submit():
        login = request.form['login']
        data = ADMIN.viewSub(login)
        if not data:
            flash('Такого пользователя нет в системе')
            return redirect(url_for('viewSub'))
        else:
            return render_template(
                'viewSub.html',
                form = form,
                data = data,
                funcs=CreateMenu(),
            )
    return render_template(
        'viewSub.html',
        form = form,
        funcs=CreateMenu(),
    )