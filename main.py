#libs
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from dateutil.relativedelta import relativedelta
import json

#classes
from classes.counter import Counter
from classes.storage import Storage
from classes.statistics import Statistics
from classes.goal import Goal


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
