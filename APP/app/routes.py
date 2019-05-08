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
def VerifyAuthData(login, password, role):
    user = None
    try:
        if role == 'coach':
            user = COACH.get((COACH.Login == login) & (COACH.Password == password))
        elif role == 'client':
            user = CLIENT.get((CLIENT.Login == login) & (CLIENT.Password == password))
        elif role == 'admin':
            user = ADMIN.get((ADMIN.Login == login) & (ADMIN.Password == password))
    except:
        return None
    return user

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

# Возвращает пользователя если он есть в БД, иначе 0
def VerifyUser(login, role):
    user = None
    try:
        if role == 'coach':
            user = COACH.get(COACH.Login == login)
        elif role == 'client':
            user = CLIENT.get(CLIENT.Login == login)
        elif role == 'admin':
            user = ADMIN.get(ADMIN.Login == login)
    except:
        return None
    return user

# Проверяет есть ли у текущего пользователя достаточно прав
def VerifyPermissions(role):
    if 'role' in session:
        if session['role'] == role:
            return 1
        else:
            flash("У вас недостаточно прав для совершения данной операции")
            return 0
    else:
        flash("Вы еще не вошли в систему")
        return 0

# Проверяет ли пустая сессия или нет (1 - да)
def checkEmptySession():
    if 'username' in session:
        return 0
    else:
        return 1


"""
            ______Маршруты______
"""


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not checkEmptySession():
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
    if not checkEmptySession():
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        login = request.form['username']
        password = request.form['password']
        role = request.form['roles']
        user = VerifyAuthData(login, password, role)
        if not user:
            flash('Вы ввели неверные данные, попробуйте еще раз')
            return redirect(url_for('login'))
        session['username'] = user.Login
        session['role'] = role
        if role != 'admin':
            session['FIO'] = user.FIO
        else:
            session['FIO'] = 'Администратор'
        flash('Вы успешно авторизовались в системе')
        return redirect(url_for('index'))
    return render_template(
        'login.html',
        form=form,
    )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if checkEmptySession():
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
    if not VerifyPermissions('coach'):
        return redirect(url_for('index'))
    coach = VerifyUser(session['username'], 'coach')
    res = coach.viewShedule()
    return render_template(
        'viewShedule.html',
        data = res,
        funcs=CreateMenu(),
    )

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
            )
    return render_template(
        'viewSub.html',
        form = form,
    )