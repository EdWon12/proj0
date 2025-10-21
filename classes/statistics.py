#libs
import datetime
import os
from kivy.app import App
from kivy.utils import platform
from os.path import join
from android.storage import app_storage_path

if platform == 'android':
    path = app_storage_path()

#classes
from classes.storage import Storage

class Statistics:
    def __init__(self):
        self.storageKey = 'current'
        self.storage = Storage(self.storageKey)
        self.key = 'timestamps'

    def persist(self):
        try:
            currentValues = self.storage.get(self.key)['value'] or []
        except:
            currentValues = []
        currentValues.append(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.storage.persist(self.key, value=currentValues)

    def archive(self):
        old_file_name = join(path, '/UserData/{self.storageKey}.json')
        if os.path.exists(old_file_name):
            os.rename(old_file_name, join(path, '/UserData/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'))
        self.__init__()