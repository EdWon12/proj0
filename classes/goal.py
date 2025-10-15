#classes
from classes.storage import Storage

class Goal:
    def __init__(self):
        self.goal = None
        self.date = None
        self.storageKey_goal = 'goal'
        self.storageKey_date = 'date'
        self.storage = Storage('goal')

        storedInfo_goal = self.storage.get(self.storageKey_goal)
        if storedInfo_goal is not None:
            self.goal = storedInfo_goal['value']

        storedInfo_date = self.storage.get(self.storageKey_date)
        if storedInfo_date is not None:
            self.date = storedInfo_date['value']

    def get(self):
        return {
            'goal': self.goal,
            'date': self.date
        }

    def set(self, goal, date):
        self.goal = goal
        self.date = date

    def persist(self):
        self.storage.persist(key=self.storageKey_goal, value=self.goal)
        self.storage.persist(key=self.storageKey_date, value=self.date)