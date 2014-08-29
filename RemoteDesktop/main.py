from kivy.app import App
from kivy.config import Config
from kivy.utils import get_color_from_hex


class RemoteDesktopApp(App):
    pass

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window  # load after Config.set
    Window.clearcolor = get_color_from_hex('#95a5a6')

    RemoteDesktopApp().run()
