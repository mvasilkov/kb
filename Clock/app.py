from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase

from time import strftime


class ClockApp(App):
    def on_start(self):
        self.update()
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.root.ids.time.text = strftime('[b]%I[/b]:%M:%S')

if __name__ == '__main__':
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Thin.ttf',
                       fn_bold='Roboto-Medium.ttf')
    ClockApp().run()
