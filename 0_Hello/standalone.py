from kivy.app import App
from kivy.uix.label import Label


class StandaloneApp(App):
    def build(self):
        return Label(text='Hello, Kivy')

if __name__ == '__main__':
    StandaloneApp().run()
