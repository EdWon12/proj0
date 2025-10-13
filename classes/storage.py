#libs
from kivy.storage.jsonstore import JsonStore

class Storage:
    def __init__(self, storageKey):
        self.storage = None
        self.load_storage(storageKey)

    def load_storage(self, storageKey):
        if self.storage == None:
            self.storage = JsonStore(f'./UserData/{storageKey}.json')

    def persist(self, key, value):
        self.storage.put(key, value=value)

    def get(self, key):
    	if self.storage.exists(key):
    		return self.storage.get(key) or None
    	else:
    		return None