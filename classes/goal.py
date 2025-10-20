#libs
from datetime import datetime

#classes
from classes.storage import Storage

class Goal:
    def __init__(self):
        self.goal = None
        self.date = None
        self.previousUsage = None
        self.previousDate = None
        self.storageKey_goal = 'goal'
        self.storageKey_date = 'date'
        self.storageKey_previousUsage = 'previousUsage'
        self.storageKey_previousDate = 'previousDate'
        self.storage = Storage('goal')

        storedInfo_goal = self.storage.get(self.storageKey_goal)
        if storedInfo_goal is not None:
            self.goal = storedInfo_goal['value']

        storedInfo_date = self.storage.get(self.storageKey_date)
        if storedInfo_date is not None:
            self.date = storedInfo_date['value']

        storedInfo_previousUsage = self.storage.get(self.storageKey_previousUsage)
        if storedInfo_previousUsage is not None:
            self.previousUsage = storedInfo_previousUsage['value']

        storedInfo_previousDate = self.storage.get(self.storageKey_previousDate)
        if storedInfo_previousDate is not None:
            self.previousDate = storedInfo_previousDate['value']

    def get(self):
        return {
            'goal': self.goal,
            'date': self.date,
            'previousUsage': self.previousUsage,
            'previousDate': self.previousDate
        }

    def set(self, goal, date, previousUsage):
        self.goal = goal
        self.date = date
        self.previousUsage = previousUsage
        self.previousDate = datetime.now().date().strftime("%d-%m-%Y")

    def persist(self):
        self.storage.persist(key=self.storageKey_goal, value=self.goal)
        self.storage.persist(key=self.storageKey_date, value=self.date)
        self.storage.persist(key=self.storageKey_previousUsage, value=self.previousUsage)
        self.storage.persist(key=self.storageKey_previousDate, value=self.previousDate)