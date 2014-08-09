from kivy.app import App
from kivy.config import Config


class ChatApp(App):
    pass

if __name__ == '__main__':
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    ChatApp().run()
