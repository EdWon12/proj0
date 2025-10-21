#libs
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from dateutil.relativedelta import relativedelta
from kivy.graphics import Color, Rectangle
from kivy.metrics import sp
from datetime import datetime, timedelta, date
from kivy.app import App
import json
import os

#classes
from classes.counter import Counter
from classes.storage import Storage
from classes.statistics import Statistics
from classes.goal import Goal

#const
date_format = "%d-%m-%Y"

#Set background color to black
Window.clearcolor = (0, 0, 0, 1)  #RGBA

class BlackThemeUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)

        #Create UserData dir
        config_path = os.path.expanduser(f'{App.get_running_app().user_data_dir}/stopsmoking/UserData/')
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        #Draw black background
        with self.canvas.before:
            Color(0, 0, 0, 1)  #Pure black
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.counter = Counter()
        self.goal = Goal()
        self.left_today = 0

        #Title label
        self.add_widget(Label(text="Please stop!", font_size=sp(24), color=(1, 1, 1, 1)))

        #Grid for inputs
        self.grid = GridLayout(cols=2, spacing=10, size_hint=[1, 1])
        self.grid.bind(minimum_height=self.grid.setter('height'))

        #Goal popup setup
        self.date_input = None
        self.popup_goals_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=([1, 1]), pos_hint={'x': 0, 'y': 0})
        self.popup_goals_layout.current_input = TextInput(hint_text='Current daily amount of smokes', input_filter='int', size_hint=([1, 0.05]), pos_hint={'x': 0, 'y': 0})
        self.popup_goals_layout.goal_input = TextInput(hint_text='Target number (best is 0)', input_filter='int', size_hint=([1, 0.05]), pos_hint={'x': 0, 'y': 0.2})
        self.popup_goals_layout.goal_close_btn = Button(text="OK", size_hint=([1, 0.05]), pos_hint={'x': 0, 'y': 0.8})
        self.popup_goals_layout.add_widget(self.popup_goals_layout.current_input)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.goal_input)

        self.popup_goals_layout.pick_button = Button(text="Select an end date for the goal", size_hint=([1, 0.05]), pos_hint={'x': 0, 'y': 0.8})
        self.popup_goals_layout.pick_button.bind(on_release=self.open_date_picker)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.pick_button)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.goal_close_btn)
        
        self.popup_goals_layout.goal_close_btn.bind(on_press=self.on_submit_goal_popup)

        self.popup_goals = Popup(title="Target goals",
                                        content=self.popup_goals_layout,
                                        size_hint=[2, 2])

        #Current count label
        self.grid.current_count = Label(text=f"Current count: {self.counter.get()}", color=(1, 1, 1, 1))
        self.grid.add_widget(self.grid.current_count)

        #Placeholder for "Left today"
        self.grid.left_today = Label(text=f"Left today: {self.left_today}", color=(1, 1, 1, 1))
        self.grid.add_widget(self.grid.left_today)

        self.add_widget(self.grid)

        #Goal popup if not set
        if self.goal.get()['goal'] is None or self.goal.get()['date'] is None:
            self.grid.add_widget(self.popup_goals)
        else:
            self.calculate_left_today()

        #Button smoke
        self.smoke_btn = Button(text="SMOKE", size_hint=([1, None]), background_color=(0.2, 0.6, 0.8, 1))
        self.smoke_btn.bind(on_press=self.on_smoke)
        self.add_widget(self.smoke_btn)

        #Button new day
        self.new_day_btn = Button(text="NEW DAY", size_hint=([1, None]), background_color=(0.2, 0.6, 0.8, 1))
        self.new_day_btn.bind(on_press=self.on_reset)
        self.add_widget(self.new_day_btn)

        #Goal Label
        goal_data = self.goal.get()
        goal_text = "unknown"

        if goal_data["goal"] is not None and goal_data["date"] is not None:
            goal_text = f"{goal_data['goal']} {goal_data['date']}"

        self.goal_label = Label(
            text=f"Goal: {goal_text}",
            color=(0.8, 0.8, 0.8, 1)
        )

        self.add_widget(self.goal_label)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def validate_goal_popup(self):
        if self.date_input is not None and self.date_input <= date.today():
            return False
        if self.popup_goals_layout.goal_input.text is not None and self.popup_goals_layout.current_input.text is not None:
            try:
                int(self.popup_goals_layout.goal_input.text)
                int(self.popup_goals_layout.current_input.text)
            except:
                return False
        return True

    def on_submit_goal_popup(self, instance):
        isValid = self.validate_goal_popup()
        if isValid is False:
            return
        self.goal.set(goal=int(self.popup_goals_layout.goal_input.text), date=self.date_input.strftime(date_format), previousUsage=int(self.popup_goals_layout.current_input.text))
        self.goal.persist()
        self.goal_label.text = f"Goal: {self.goal.get()['goal']} {self.date_input.strftime(date_format)}"
        self.close_goals_popup()
        self.calculate_left_today()

    def on_smoke(self, instance):
        self.counter.increment()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"
        self.calculate_left_today()

    def on_reset(self, instance):
        self.counter.reset()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"
        self.calculate_left_today()

    def open_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()
    
    def close_goals_popup(self, *args):
        if self.popup_goals:
            self.grid.remove_widget(self.popup_goals)

    def on_date_selected(self, instance, value, date_range):
        self.date_input = value
    
    def calculate_left_today(self):
        goals = self.goal.get()
        goal = goals['goal']
        date = datetime.strptime(goals['date'], date_format).date()
        previousUsage = goals['previousUsage']
        previousDate = datetime.strptime(goals['previousDate'], date_format).date()
        now = date.today()

        total_diff = (date - now).days
        goal_diff = self.goal.get()['previousUsage'] - self.goal.get()['goal']

        reduction_rate =  goal_diff / total_diff
        
        self.left_today = round(previousUsage - (max(1, (now - previousDate).days) * reduction_rate)) - self.counter.get()
        
        self.grid.left_today.text = f"Left today: {self.left_today}"

class BlackApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return BlackThemeUI()

if __name__ == '__main__':
    from kivy.logger import Logger
    try:
        Logger.info("App starting")
        BlackApp().run()
        Logger.info("App ended")
    except Exception as e:
        Logger.error(f"BlackApp: Uncaught exception: {e}")


