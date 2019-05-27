import datetime
from peewee import *
from app import db
from datetime import datetime, timedelta

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
        for el in DEPARTMENT.select().order_by(DEPARTMENT.City):
            deplist.append((str(el.ID), "{}, {}".format(el.City, el.Address)))
        return deplist

# Админы
class ADMIN(IUser, IElement):

    def addSub(self, client, days):
        flag = False
        sub = 0
        # Если нет абонемента, то создадим его
        try:
            sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == client.Sub_ID)
        except:
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

    def viewSub(self, client):
        isExistsSub = True
        FIO = client.FIO
        try:
            sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == client.Sub_ID)
            days = sub.WorkoutsCount - sub.CompletedWorkouts
            return list([isExistsSub, FIO, days])
        except:
            return list([isExistsSub, FIO])

# Клиенты клуба
class CLIENT(IUser, IElement):
    FIO = FixedCharField(100)
    Sub_ID = ForeignKeyField(
        SUBSCRIPTION,
        db_column='Sub_ID'
    )
    def recording(self, time, coach, activity):
        sub_id = self.getSubObject().ID
        print("номер: {}".format(sub_id))
        sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == sub_id)
        newcount = sub.CompletedWorkouts + 1
        SUBSCRIPTION.update(CompletedWorkouts=newcount).where(SUBSCRIPTION.ID == sub).execute()
        try:
            index = TRAINING.insert(
                Start_time = time.strftime('%d.%m.%Y %H:%M'),
                Client_ID = self.ID,
                Coach_ID = coach.ID,
                Activity_ID = activity.ID,
            ).execute()

            return 1
        except:
            return 0

    def viewWorkouts(self):
        data = []
        for el in TRAINING.select().where(TRAINING.Client == self.ID).order_by(TRAINING.Start_time.desc()):
            date_obj = datetime.strptime(el.Start_time, '%d.%m.%Y %H:%M')
            finishtime = date_obj + timedelta(hours=1)
            fio = COACH.get(COACH.id == el.Coach_ID).FIO
            activity = ACTIVITY.get(ACTIVITY.ID == el.Activity_ID).Title
            venue = ACTIVITY.get(ACTIVITY.ID == el.Activity_ID).Venue_Title
            coachdep = COACH.get(COACH.id == el.Coach_ID).Dep
            dep = DEPARTMENT.get(DEPARTMENT.ID == coachdep).Address
            data.append((
                el.ID,
                date_obj.strftime('%d.%m.%Y'),
                date_obj.strftime('%H:%M'),
                finishtime.strftime('%H:%M'),
                fio,
                activity,
                venue,
                dep,
                date_obj.strftime('%Y.%m.%d'),
             ))
        result = sorted(data, key=lambda t: t[8], reverse=True)
        return result

    # 0 - ошибка
    def getSubObject(self):
        try:
            sub = SUBSCRIPTION.get(SUBSCRIPTION.ID == self.Sub_ID)
        except:
            return 0
        return sub



# Тренера
class COACH(IUser, IElement):
    FIO = FixedCharField(100)
    Dep = ForeignKeyField(
        DEPARTMENT,
        db_column='Dep'
    )

    def viewShedule(self):
        data = []
        for el in TRAINING.select().where(TRAINING.Coach == self.ID).order_by(TRAINING.Start_time.desc()):
            date_obj = datetime.strptime(el.Start_time, '%d.%m.%Y %H:%M')
            fio = CLIENT.get(CLIENT.id == el.Client_ID).FIO
            activity = ACTIVITY.get(ACTIVITY.ID == el.Activity_ID).Title
            venue = ACTIVITY.get(ACTIVITY.ID == el.Activity_ID).Venue_Title
            data.append((date_obj.strftime('%d.%m.%Y'),
                         date_obj.strftime('%H:%M'),
                         fio,
                         activity,
                         venue,
                         ))
        return data

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
    Coach = ForeignKeyField(COACH, db_column='Coach_ID')
    Activity = ForeignKeyField(ACTIVITY, db_column='Activity_ID')

    class Meta:
        primary_key = CompositeKey('Coach_ID','Activity_ID')

# Тренировки
class TRAINING(IElement):
    Start_time = DateTimeField(formats='%d.%m.%Y %H:%M')
    Client = ForeignKeyField(CLIENT, db_column='Client_ID')
    Coach = ForeignKeyField(COACH, db_column='Coach_ID')
    Activity = ForeignKeyField(ACTIVITY, db_column='Activity_ID')