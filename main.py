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
from datetime import datetime, timedelta

import json

#classes
from classes.counter import Counter
from classes.storage import Storage
from classes.statistics import Statistics
from classes.goal import Goal

#Set background color to black
Window.clearcolor = (0, 0, 0, 1)  #RGBA

#TODO the ui and main algorithm
class BlackThemeUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)

        #Draw black background
        with self.canvas.before:
            Color(0, 0, 0, 1)  #Pure black
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.counter = Counter()
        self.goal = Goal()

        print(f"the goal value {self.goal.get()}")

        #Title label
        self.add_widget(Label(text="Please stop!", font_size=24, color=(1, 1, 1, 1)))

        #Grid for inputs
        self.grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        #Goal popup setup
        self.popup_goals_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, height=500, width=500)
        self.popup_goals_layout.goal_input = TextInput(hint_text='Target number (best is 0)', size_hint_y=None, height=30, input_filter='int')
        self.label = Label(text="Select a target date for the Goal")
        self.popup_goals_layout.goal_close_btn = Button(text="OK", size_hint=(1, None), height=50)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.goal_input)

        self.popup_goals_layout.pick_button = Button(text="Select an end date for the goal")
        self.popup_goals_layout.pick_button.bind(on_release=self.open_date_picker)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.pick_button)
        self.popup_goals_layout.add_widget(self.popup_goals_layout.goal_close_btn)
        
        self.popup_goals_layout.goal_close_btn.bind(on_press=self.on_submit)

        self.popup_goals = Popup(title="Goals popup",
                                        content=self.popup_goals_layout,
                                        size_hint=(None, None),
                                        size=(400, 300),
                                        auto_dismiss=False)

        #Goal popup if not set
        if self.goal.get()['goal'] is None or self.goal.get()['date'] is None:
            self.grid.add_widget(self.popup_goals)

        #Current count label
        self.grid.current_count = Label(text=f"Current count: {self.counter.get()}", color=(1, 1, 1, 1))
        self.grid.add_widget(self.grid.current_count)

        #Placeholder for "Left today"
        self.grid.add_widget(Label(text="Left today:", color=(1, 1, 1, 1)))

        self.add_widget(self.grid)

        #Button smoke
        self.smoke_btn = Button(text="SMOKE", size_hint=(1, None), height=50, background_color=(0.2, 0.6, 0.8, 1))
        self.smoke_btn.bind(on_press=self.on_smoke)
        self.add_widget(self.smoke_btn)

        #Button new day
        self.new_day_btn = Button(text="NEW DAY", size_hint=(1, None), height=50, background_color=(0.2, 0.6, 0.8, 1))
        self.new_day_btn.bind(on_press=self.on_reset)
        self.add_widget(self.new_day_btn)

        #Goal Label
        self.goal_label = Label(text=f'Goal: {'unkown' if self.goal.get()['goal'] is None or self.goal.get()['date'] is None else f"{self.goal.get()['goal']} {self.goal.get()['date']}"}', color=(0.8, 0.8, 0.8, 1))
        self.add_widget(self.goal_label)

        #TODO add left for today

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_submit(self, instance):
        self.goal.set(goal=int(self.popup_goals_layout.goal_input.text), date=self.date_input.strftime("%d-%m-%Y"))
        self.goal.persist()
        self.goal_label.text = f"Goal: {self.goal.get()['goal']} {self.date_input.strftime("%d-%m-%Y")}"
        self.close_goals_popup()

    def on_smoke(self, instance):
        self.counter.increment()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"

    def on_reset(self, instance):
        self.counter.reset()
        self.grid.current_count.text = f"Current count: {self.counter.get()}"

    def open_date_picker(self, instance):
        print(datetime.now().date() + timedelta(days=1))
        date_picker = MDDatePicker(min_date=datetime.now().date() + timedelta(days=1)) #TODO: min date not working
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()
    
    def close_goals_popup(self, *args):
        if self.popup_goals:
            self.grid.remove_widget(self.popup_goals)

    def on_date_selected(self, instance, value, date_range):
        self.date_input = value
class BlackApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return BlackThemeUI()

if __name__ == '__main__':
    BlackApp().run()

#now = datetime.now()
#next_month = now + relativedelta(months=1)

