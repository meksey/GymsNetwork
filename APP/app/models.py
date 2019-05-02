import datetime
from peewee import *
from app import db

# Интрефейс Базовой модели
class BaseModel(Model):
    class Meta:
        database = db

# Интерфейс сущности пользователь
class IUser(BaseModel):
    Login = FixedCharField(20)
    Password = FixedCharField(20)

    def exit(self):
        pass

# Интерфейс сущности элемент системы
class IElement(BaseModel):
    ID = AutoField()


# Абонемент
class SUBSCRIPTION(IElement):
    WorkoutsCount = IntegerField(default=30)
    CompletedWorkouts = IntegerField(default=0)

# Филиал клуба
class DEPARTMENT(IElement):
    City = FixedCharField(45)
    Address = FixedCharField(250)

    @staticmethod
    def getDepList():
        deplist = []
        for el in DEPARTMENT.select():
            deplist.append((str(el.ID), "{}, {}".format(el.City, el.Address)))
        return deplist

# Админы
class ADMIN(IUser, IElement):
    @staticmethod
    def addSub(client, days):
        flag = False
        sub = 0
        # Если нет абонемента, то создадим его
        try:
            sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == client.Sub_ID)
        except:
            print("Не удалось найти абонемент у пользователя {}".format(client.Login))
            flag = True
        if flag:
            sub_id = SUBSCRIPTION.insert(WorkoutsCount = days,
                                CompletedWorkouts = 0).execute()
            CLIENT.update(Sub_ID = sub_id).where(CLIENT.Login == client.Login).execute()
            return 1
        else:
            newdays = sub.WorkoutsCount + days
            print(newdays)
            SUBSCRIPTION.update(WorkoutsCount = newdays).where(SUBSCRIPTION.ID == client.Sub_ID).execute()
            return 1

    # 0: такого пользователя нет
    @staticmethod
    def viewSub(login):
        try:
            CLIENT.get(CLIENT.Login == login)
        except:
            print('Пользователь {} не найден'.format(login))
            return 0
        isExistsSub = True
        client = CLIENT.get(CLIENT.Login == login)
        login = client.Login
        FIO = client.FIO
        sub = None
        try:
            sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == client.Sub_ID)
        except:
            print("Не удалось найти абонемент у пользователя {}".format(client.Login))
            isExistsSub = False
        if isExistsSub:
            days = sub.WorkoutsCount - sub.CompletedWorkouts
            return list([isExistsSub, FIO, days])
        else:
            return list([isExistsSub, FIO])






# Клиенты клуба
class CLIENT(IUser, IElement):
    FIO = FixedCharField(100)
    Sub_ID = ForeignKeyField(
        SUBSCRIPTION,
        db_column='Sub_ID'
    )
    def recording(self):
        pass

# Тренера
class COACH(IUser, IElement):
    FIO = FixedCharField(100)
    Dep = ForeignKeyField(
        DEPARTMENT,
        db_column='Dep'
    )
    def viewShedule(self):
        pass

# Активности
class ACTIVITY(IElement):
    Title = FixedCharField(45)
    Venue_Title = FixedCharField(45)

    @staticmethod
    def getActivities():
        actlist = []
        for el in ACTIVITY.select():
            actlist.append((str(el.ID), el.Title))
        return actlist

# Активность тренера
class COACH_ACTIVITY(BaseModel):
    Coach_ID = ForeignKeyField(COACH, db_column='Coach_ID')
    Activity_ID = ForeignKeyField(ACTIVITY, db_column='Activity_ID')

    class Meta:
        primary_key = CompositeKey('Coach_ID','Activity_ID')

# Тренировки
class TRAINING(IElement):
    Start_time = DateTimeField()
    Client_ID = ForeignKeyField(CLIENT, db_column='ID')
    Coach_ID = ForeignKeyField(COACH, db_column='ID')
    Activity_ID = ForeignKeyField(ACTIVITY, db_column='ID')