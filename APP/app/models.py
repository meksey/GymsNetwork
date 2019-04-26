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
    FIO = FixedCharField(100)

    def exit(self):
        pass

# Интерфейс сущности элемент системы
class IElement(BaseModel):
    ID = AutoField(primary_key=True)


# Филиал клуба
class DEPARTMENT(IElement):
    City = FixedCharField(45)
    Address = FixedCharField(250)

# День недели
class WEEKDAY(IElement):
    Title = FixedCharField(20)

# Уровни абонемента
class LEVELS(IElement):
    Trainings = IntegerField(default=30)
    LevelName = FixedCharField(30)
    Price = IntegerField()


# Админы
class ADMIN(IUser, IElement):
    def monitorCard(self):
        pass

    def getCoaches(self):
        pass

# Клиенты клуба
class CLIENT(IUser, IElement):
    BirthDate = DateField(format("%d-%m-%Y"))
    SubLevel = ForeignKeyField(LEVELS, db_column='ID')
    SubSrartDate = DateField(format("%d-%m-%Y"), default=datetime.date.today())
    TrainingsCount = IntegerField(default=0)

    def recording(self):
        pass

# Тренера
class COACH(IUser, IElement):
    BirthDate = DateField(format("%d-%m-%Y"))
    Price = IntegerField()
    Dep_ID = ForeignKeyField(
        DEPARTMENT,
        db_column='ID'
    )

    def viewShedule(self):
        pass
    def changePrice(self):
        pass



# Активности
class ACTIVITY(IElement):
    Title = FixedCharField(45)
    Venue_Title = FixedCharField(45)

# Активность тренера
class COACH_ACTIVITY(BaseModel):
    Coach_ID = ForeignKeyField(COACH, db_column='ID')
    Activity_ID = ForeignKeyField(ACTIVITY, db_column='ID')

    class Meta:
        primary_key = CompositeKey('Coach_ID','Activity_ID')

# Тренировки
class TRAINING(IElement):
    Start_time = DateTimeField()
    Date = DateField(format("%d-%m-%Y"))
    Client_ID = ForeignKeyField(CLIENT, db_column='ID')
    Coach_ID = ForeignKeyField(COACH, db_column='ID')
    Activity_ID = ForeignKeyField(ACTIVITY, db_column='ID')

# Рабочий день тренера
class WORK_DAY(BaseModel):
    Coach_ID = ForeignKeyField(COACH, db_column='ID')
    Weekday_ID = ForeignKeyField(WEEKDAY, db_column='ID')

    class Meta:
        primary_key = CompositeKey('Coach_ID', 'Weekday_ID')