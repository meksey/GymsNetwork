from app import app, api, ns_client, ns_coach, Resource
from flask import render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegAsClientForm, RegAsCoachForm, AddSub, ViewSub, RecordForm
from app.models import CLIENT, SUBSCRIPTION, COACH, ADMIN, DEPARTMENT, COACH_ACTIVITY, TRAINING, ACTIVITY
from datetime import datetime, timedelta

# Добавить тренера (0 если не удалось)
def addCoach(fio, login, password, dep, acts):
    try:
        COACH.insert(FIO=fio,
                     Login=login,
                     Password=password,
                     Dep=dep).execute()
        coach = VerifyUser(login, 'coach')
        for act in acts:
            COACH_ACTIVITY.insert(Coach_ID = coach.ID, Activity_ID = act).execute()
        return 1
    except:
        return 0

# Добавить клиента (1 - удачно, 0 - неудачно)
def addClient(fio, login, password):
    try:
        CLIENT.insert(FIO=fio,
                      Login=login,
                      Password=password,
                      ).execute()
        return 1
    except:
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
    if 'role' not in session:
        return func
    if session['role'] == 'coach':
        func = [('viewShedule', 'Расписание тренеровок'),
                ]
    elif session['role'] == 'client':
        func = [('recording','Запись на тренировку'),
                ('viewWorkouts', 'Расписание тренировок')
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

# Метод составляет списо тренеров по параметрам записи на тренировку
def getCoachesForTraining(department, activity, time):
    fil_act = []
    # Выборка тренеров по activity
    for el in COACH_ACTIVITY.select().where(COACH_ACTIVITY.Activity_ID == activity):
        fil_act.append(el.Coach_ID)
    # ВЫборка по времени (Заданное время)
    time_of_training = timedelta(hours=1)
    time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M')    # Заданное время
    print("Список тренеров после отсеивания по типу тренирвоки: {}".format(fil_act))
    for el in TRAINING.select().where((TRAINING.Coach << fil_act)):
        el_time = datetime.strptime(el.Start_time, '%d.%m.%Y %H:%M')    # Время просматриваемой тренировки
        if not ((time_obj >= (el_time + time_of_training)) or ((time_obj + time_of_training) <= el_time)) :
            fil_act.remove(el.Coach_ID)
            print("Тренировка {} накладывается поэтому тренер {} удален из подборки".format(el.ID, el.Coach_ID))
    print("Список оставшихся тренеров: {}".format(fil_act))
    coaches = COACH.select().where((COACH.Dep == department) & (COACH.id << fil_act))
    for el in coaches:
        print('---------------')
        print("Тренер №: {}".format(el.ID))
        print(el.FIO)
        print("Номер его отделения: {}".format(el.Dep))
    return coaches









"""
            ______Маршруты______
"""


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not checkEmptySession():
        return render_template(
            'index.html',
            funcs=CreateMenu(),
            user = 1,
        )
    else:
        return render_template(
            'index.html',
            user=0,
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
        user=0,
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
    if not checkEmptySession():
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))
    form = RegAsClientForm()
    if form.validate_on_submit():
        fio = request.form['fio']
        login = request.form['username']
        password = request.form['password']
        client = VerifyUser(login, 'client')
        if client:
            flash('Такой пользователь уже существует')
            return redirect(url_for('index'))
        if not addClient(fio, login, password):
            flash('Не удалось добавить такого пользователя в систему')
            return redirect(url_for('regasclient'))
        session['username'] = login
        session['FIO'] = fio
        session['role'] = 'client'
        flash('Вы успешно зарегистрировались в системе')
        return redirect(url_for('index'))
    return render_template(
        'regasclient.html',
        form = form,
        user = 0,
    )

@app.route('/regascoach', methods=['GET', 'POST'])
def regascoach():
    if not checkEmptySession():
        flash('Вы уже авторизовались в системе')
        return redirect(url_for('index'))
    form = RegAsCoachForm()
    if form.validate_on_submit():
        fio = request.form['fio']
        login = request.form['username']
        password = request.form['password']
        department = form.department.data
        activity = form.activity.data
        coach = VerifyUser(login, 'coach')
        if coach:
            flash('Такой пользователь уже существует')
            return redirect(url_for('index'))
        if not addCoach(fio, login, password, department, activity):
            flash('Не удалось добавить такого пользователя в систему')
            return redirect(url_for('regascoach'))
        session['username'] = login
        session['FIO'] = fio
        session['role'] = 'coach'
        flash('Вы успешно зарегистрировались в системе')
        return redirect(url_for('index'))
    return render_template(
        'regascoach.html',
        form=form,
        user=0,
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
        user=1,
    )

@app.route('/addSub', methods=['GET', 'POST'])
def addSub():
    if not VerifyPermissions('admin'):
        return redirect(url_for('index'))
    form = AddSub()
    if form.validate_on_submit():
        login = request.form['login']
        days = int(request.form['days'])
        if (days <= 0) or (days >250):
            flash('Введено недопустимое количество дней')
            return redirect(url_for('addSub'))
        client = VerifyUser(login, 'client')
        if not client:
            flash('Данный пользователь не существует')
            return redirect(url_for('addSub'))
        admin = VerifyUser(session['username'], 'admin')
        print(session['username'])
        if (admin.addSub(client, days)):
            flash('Информация успешно обновлена')
            return redirect(url_for('index'))
    return render_template(
        'addSub.html',
        form=form,
        funcs=CreateMenu(),
        user=1,
    )

@app.route('/viewSub', methods=['GET', 'POST'])
def viewSub():
    if not VerifyPermissions('admin'):
        return redirect(url_for('index'))
    form = ViewSub()
    if form.validate_on_submit():
        login = request.form['login']
        client = VerifyUser(login, 'client')
        if not client:
            flash('Данный пользователь не существует')
            return redirect(url_for('viewSub'))
        admin = VerifyUser(session['username'], 'admin')
        data = admin.viewSub(client)
        if not data:
            flash('Не удалось посмотреть аккаунт клиента')
            return redirect(url_for('viewSub'))
        else:
            return render_template(
                'viewSub.html',
                form = form,
                data = data,
                funcs=CreateMenu(),
                user=1,
            )
    return render_template(
        'viewSub.html',
        form = form,
        funcs=CreateMenu(),
        user=1,
    )


department = None
activity = None
time = None

@app.route('/recording', methods=['GET', 'POST'])
def recording():
    if not VerifyPermissions('client'):
        return redirect(url_for('index'))
    form = RecordForm()
    client = VerifyUser(session['username'], 'client')
    if (( not client.getSubObject()) or ((client.getSubObject().WorkoutsCount - client.getSubObject().CompletedWorkouts) <= 0)):
        flash(
            'К сожалению, у вас не осталось тренировок на аккаунте. Обратитесь к администратору клуба для пополнения.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        global department
        global activity
        global time
        department = form.department.data
        activity = form.activity.data
        time = request.form['start_time']

        try:
            time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        except:
            flash('Введите дату и время правильно.')
            return redirect(url_for('recording'))
        now = datetime.now()
        if(time_obj<=now):
            flash('Вы не можете записаться на тренировку в прошлом.')
            return redirect(url_for('recording'))
        if(time_obj.hour <= 8 or time_obj.hour >= 23):
            flash('Выберите другое время, фитнесс центр работает с 10:00 до 23:00.')
            return redirect(url_for('recording'))
        list_coaches = getCoachesForTraining(department, activity, time)
        if not list_coaches:
            flash("Извините, подходящих тренеров не найдено")
            return redirect(url_for('recording'))
        return render_template(
            'recording_result.html',
            funcs = CreateMenu(),
            coaches = list_coaches,
            user=1,
        )
    return render_template(
        'record.html',
        form=form,
        funcs=CreateMenu(),
        user=1,
    )

@app.route('/recordingRes', methods=['GET', 'POST'])
def recordingRes():
    global activity
    global time
    if (request.form):
        coach = COACH.get(COACH.id == request.form['index'])    # Объект тренера
        client = VerifyUser(session['username'], 'client')      # Объект клиента
        act = ACTIVITY.get(ACTIVITY.ID == activity)             # Объект деятельности
        time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M')    # Объект времени
        if client.recording(time_obj, coach, act):
            flash("Вы успешно записались на тренировку.")
            return redirect(url_for('recording'))
        else:
            flash("Не получилось записать вас на тренировку.")
            return redirect(url_for('recording'))
    else:
        flash("Сначала введите все данные")
        return redirect(url_for('recording'))

@app.route('/viewWorkouts', methods=['GET', 'POST'])
def viewWorkouts():
    if not VerifyPermissions('client'):
        return redirect(url_for('index'))
    client = VerifyUser(session['username'], 'client')
    res = client.viewWorkouts()
    return render_template(
        'viewWorkouts.html',
        data = res,
        funcs = CreateMenu(),
        user=1,
    )

@app.route('/delWorlout', methods=['GET', 'POST'])
def DelWorkout():
    if not VerifyPermissions('client'):
        return redirect(url_for('index'))
    if not 'id' in request.form:
        flash("Вы еще не выбрали какую тренировку удалять!")
        return redirect(url_for('index'))
    workout = TRAINING.get(TRAINING.ID == request.form['id'])
    workout.delete_instance()
    flash("Тренировка {} успешно удалена!".format(request.form['id']))
    return redirect(url_for('index'))

@app.route('/about', methods=['GET', 'POST'])
def about():
    user = 0
    if 'username' in session:
        user = 1
    return render_template(
        'about.html',
        funcs=CreateMenu(),
        user=user,
    )

"""
            ______API______
"""
@ns_client.route('All')
class api_client_all(Resource):
    def get(self):
        """Вернуть данные о всех пользователях системы"""
        res = []
        for el in CLIENT.select():
            res.append(
                {
                    'ФИО': str(el.FIO),
                    'Логин в системе': str(el.Login),
                    'ID клиента': str(el.ID),
                    'ID абонемента': str(el.Sub_ID),
                }
            )
        return res

@ns_client.route('Current')
class api_client_current(Resource):
    def get(self):
        """Вернуть данные о текущем пользователе"""
        if 'username' not in session:
            return "ERROR: no user in session"
        client = CLIENT.get(CLIENT.Login == session['username'])
        res = {
            'ФИО': str(client.FIO),
            'Логин в системе': str(client.Login),
            'ID клиента': str(client.ID),
            'ID абонемента': str(client.Sub_ID),
        }
        return res
