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

# Админы
class ADMIN(IUser, IElement):
    @staticmethod
    def addSub(client, days):

    def getCoaches(self):
        pass

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