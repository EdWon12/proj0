#libs
import datetime
import os
from kivy.app import App

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
        old_file_name = f'{App.get_running_app().user_data_dir}/stopsmoking/UserData/{self.storageKey}.json'
        if os.path.exists(old_file_name):
            os.rename(old_file_name, f'{App.get_running_app().user_data_dir}/stopsmoking/UserData/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json')
        self.__init__()