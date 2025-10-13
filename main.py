from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup

from kivy.storage.jsonstore import JsonStore
from dateutil.relativedelta import relativedelta
import datetime
import json
import os


# Set background color to black
Window.clearcolor = (0, 0, 0, 1)  # RGBA


# TODO the ui and main alghorithm
class BlackThemeUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)



        self.counter = Counter()

        self.title = Label(text="Please stop!",
                           font_size=24, color=(1, 1, 1, 1))
        self.add_widget(self.title)

        # Grid for inputs
        self.grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.goal = Goal()

        print(f"the goal value{self.goal.get()}")

        if self.goal.get() is None:
            self.popup_goals = BoxLayout(orientation='vertical', spacing=10, padding=10)
            self.popup_goals.goal_input = TextInput(hint_text='Target number (best is 0)')
            self.popup_goals.goalDate_input = TextInput(hint_text='Target date for the Goal')
            self.popup_goals.goal_close_btn = Button(text="OK", size_hint=(1, None), height=50)
            self.popup_goals.popup = Popup(title="Goals popup",
                      content=self.popup_goals,
                      size_hint=(None, None),
                      size=(400, 200))
            self.popup_goals.goal_close_btn.bind(on_press = self.popup_goals.popup.dismiss)
            self.popup_goals.add_widget(self.popup_goals.goal_input, self.popup_goals.goalDate_input, self.popup_goals.goal_close_btn)
            self.add_widget(self.popup_goals.popup)

        self.grid.current_count = Label(text=f"Current count: {self.counter.get()}", color=(1, 1, 1, 1))

        self.grid.add_widget(self.grid.current_count)

        self.grid.add_widget(Label(text="Left today:", color=(1, 1, 1, 1)))

        self.add_widget(self.grid)

        # Button smoke
        self.smoke_btn = Button(text="SMOKE", size_hint=(
            1, None), height=50, background_color=(0.2, 0.6, 0.8, 1))
        self.smoke_btn.bind(on_press=self.on_smoke)
        self.add_widget(self.smoke_btn)


        # Button new day
        self.new_day_btn = Button(text="NEW DAY", size_hint=(
            1, None), height=50, background_color=(0.2, 0.6, 0.8, 1))
        self.new_day_btn.bind(on_press=self.on_reset)
        self.add_widget(self.new_day_btn)

        # Output Label
        self.output = Label(text="Goal", color=(0.8, 0.8, 0.8, 1))
        self.add_widget(self.output)

        #TODO add left for today

    # def on_submit(self, instance):
    #     self.output.text = f"Hello {name}, your Left today is {Left today}"

    def on_smoke(self, instance):
        self.counter.increment()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"

    def on_reset(self, instance):
        self.counter.reset()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"




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
        old_file_name = f'{self.storageKey}.json'
        if os.path.exists(old_file_name):
            os.rename(old_file_name, f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json')
        self.__init__()


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
        try:
            Statistics().archive()
            self.counter = 0
            self.persist()
        except:
            print("error") #TODO: proper popout message when the user clicks twice the same minute


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

class BlackApp(App):
    def build(self):
        # counter = Counter()
        # print(f'Counter1: {counter.get()}')
        # counter.increment()
        # print(f'Counter2: {counter.get()}')
        # counter.persist()

        return BlackThemeUI()


if __name__ == '__main__':
    BlackApp().run()


#now = datetime.now()
#next_month = now + relativedelta(months=1)
