#classes
from classes.storage import Storage

class Goal:
    def __init__(self):
        self.goal = None
        self.goalDate = None
        self.storageKey_goal = 'goal'
        self.storageKey_goalDate = 'goalDate'
        self.storage = Storage('goals')

        self.storage_goal = Storage(self.storageKey_goal)
        self.storage_goalDate = Storage(self.storageKey_goalDate)

        storedInfo_goal = self.storage.get(self.storageKey_goal)
        if storedInfo_goal is not None:
            self.goal = storedInfo_goal['value']

        storedInfo_goalDate = self.storage.get(self.storageKey_goalDate)
        if storedInfo_goalDate is not None:
            self.goal = storedInfo_goalDate['value']

    def get(self):
        return self.goal

    def set(self, goal):
        self.goal = goal

    def persist(self):
        self.storage_goal.persist(key=self.storageKey_goal, value=self.goal)
        self.storage_goalDate.persist(key=self.storageKey_goalDate, value=self.goalDate)