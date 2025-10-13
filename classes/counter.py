#libs
import os

#classes
from classes.storage import Storage
from classes.statistics import Statistics

class Counter:
    def __init__(self):
        self.counter = 0
        self.storageKey = 'counter'
        self.storage = Storage(self.storageKey)
        storedInfo = self.storage.get(self.storageKey)
        if storedInfo is not None:
            self.counter = storedInfo['value'] or 0

    def persist(self):
        self.storage.persist(key=self.storageKey, value=self.counter)

    def increment(self):
        self.counter += 1
        self.storage.persist(key=self.storageKey, value=self.counter)
        Statistics().persist()

    def get(self):
        return self.counter

    def reset(self):
        Statistics().archive()
        self.counter = 0
        self.persist()