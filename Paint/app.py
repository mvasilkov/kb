from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class CanvasWidget(Widget):
    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            Color(*get_color_from_hex('#0080ff80'))
            Line(circle=(touch.x, touch.y, 25), width=4)


class PaintApp(App):
    def build(self):
        return CanvasWidget()

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#ffffff')
    PaintApp().run()
