from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase


class RecorderApp(App):
    pass

if __name__ == '__main__':
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')

    RecorderApp().run()
