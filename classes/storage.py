#libs
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.utils import platform
from os.path import join
from android.storage import app_storage_path

if platform == 'android':
    path = app_storage_path()

class Storage:
    def __init__(self, storageKey):
        self.storage = None
        self.load_storage(storageKey)

    def load_storage(self, storageKey):
        if self.storage == None:
            #self.storage = JsonStore(f'./UserData/{storageKey}.json')     -- for dev on pc
            self.storage = JsonStore(join(path, '/UserData/{storageKey}.json'))

    def persist(self, key, value):
        self.storage.put(key, value=value)

    def get(self, key):
    	if self.storage.exists(key):
    		return self.storage.get(key) or None
    	else:
    		return None