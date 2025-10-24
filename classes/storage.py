#libs
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.utils import platform
from os.path import join

if platform == 'android':
    from android.storage import app_storage_path
    path = app_storage_path()
else:
    path = './'

class Storage:
    def __init__(self, storageKey):
        self.storage = None
        self.load_storage(storageKey)

    def load_storage(self, storageKey):
        if self.storage == None:
            self.storage = JsonStore(join(path, f'UserData/{storageKey}.json'))

    def persist(self, key, value):
        self.storage.put(key, value=value)

    def get(self, key):
    	if self.storage.exists(key):
    		return self.storage.get(key) or None
    	else:
    		return None
