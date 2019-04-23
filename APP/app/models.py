import datetime
from peewee import *
from app import db

class BaseModel(Model):
    class Meta:
        database = db


# Филиал клуба
class DEPARTMENT(BaseModel):
    Dep_ID = PrimaryKeyField()
    City = FixedCharField(45)
    Address = FixedCharField(250)


# День недели
class WEEKDAY(BaseModel):
    Weekday_ID = PrimaryKeyField()
    Title = FixedCharField(20)


# Уровни абонемента
class LEVELS(BaseModel):
    Level = PrimaryKeyField()
    Trainings = IntegerField()
    LevelName = FixedCharField(30)
    Price = IntegerField()


# Админы
class ADMIN(BaseModel):
    Login = FixedCharField(20, primary_key=True)
    FIO = FixedCharField(100)
    Password = FixedCharField(20)


# Активности
class ACTIVITY(BaseModel):
    Activity_ID = PrimaryKeyField()
    Title = FixedCharField(45)
    Venue_Title = FixedCharField(45)
    Venue_Description = FixedCharField(100)


# Клиенты клуба
class CLIENT(BaseModel):
    Client_ID = PrimaryKeyField()
    Login = FixedCharField(25)
    Password = FixedCharField(25)
    BirthDate = DateField()
    Sub_ID = IntegerField()
    SubLevel = ForeignKeyField(LEVELS, db_column='SubLevel')
    SubSrartDate = DateField()
    FIO = FixedCharField(100)
    TrainingsCount = IntegerField()



# Тренера
class COACH(BaseModel):
    Coach_ID = PrimaryKeyField()
    Login = FixedCharField(20)
    Password = FixedCharField(20)
    FIO = FixedCharField(45)
    BirthDate = DateField()
    Price = IntegerField()
    Dep_ID = ForeignKeyField(
        DEPARTMENT,
        db_column='Dep_ID',
    )


# Активность тренера
class COACH_ACTIVITY(BaseModel):
    Coach_ID = ForeignKeyField(COACH)
    Activity_ID = ForeignKeyField(ACTIVITY)

    class Meta:
        primary_key = CompositeKey('Coach_ID','Activity_ID')


# Тренировки
class TRAINING(BaseModel):
    Training_ID = PrimaryKeyField()
    Start_time = DateTimeField()
    Client_ID = ForeignKeyField(CLIENT)
    Coach_ID = ForeignKeyField(COACH)
    Activity_ID = ForeignKeyField(ACTIVITY)


# Рабочий день тренера
class WORK_DAY(BaseModel):
    Coach = ForeignKeyField(COACH)
    Weekday = ForeignKeyField(WEEKDAY)