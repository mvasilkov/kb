from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.graphics import Color, Line
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

CURSOR = (
    '       @@@@             ',
    '       @--@             ',
    '       @--@             ',
    '       @--@             ',
    '       @--@             ',
    '       @@@@             ',
    '                        ',
    '@@@@@@ @@@@ @@@@@@      ',
    '@----@ @--@ @----@      ',
    '@----@ @--@ @----@      ',
    '@@@@@@ @@@@ @@@@@@      ',
    '                        ',
    '       @@@@             ',
    '       @--@             ',
    '       @--@             ',
    '       @--@             ',
    '       @--@             ',
    '       @@@@             ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
)


class CanvasWidget(Widget):
    line_width = 2

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            touch.ud['current_line'] = Line(
                points=(touch.x, touch.y),
                width=self.line_width)

    def on_touch_move(self, touch):
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)

    def set_color(self, new_color):
        self.last_color = new_color
        self.canvas.add(Color(*new_color))

    def set_line_width(self, line_width='Normal'):
        self.line_width = {
            'Thin': 1, 'Normal': 2, 'Thick': 4
        }[line_width]

    def clear_canvas(self):
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)
        self.set_color(self.last_color)


class PaintApp(App):
    def build(self):
        EventLoop.ensure_window()
        if EventLoop.window.__class__.__name__.endswith('Pygame'):
            try:
                from pygame import mouse

                a, b = pygame_compile_cursor()
                mouse.set_cursor((24, 24), (9, 9), a, b)
            except:
                pass

        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_color(
            get_color_from_hex('#2980b9'))
        return self.canvas_widget


class RadioButton(ToggleButton):
    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)


def pygame_compile_cursor(black='@', white='-'):
    aa, bb = [], []
    a = b = 0
    i = 8
    for s in CURSOR:
        for c in s:
            a <<= 1
            b <<= 1
            i -= 1
            if c == black:
                a |= 1
                b |= 1
            elif c == white:
                b |= 1

            if not i:
                aa.append(a)
                bb.append(b)
                a = b = 0
                i = 8

    return tuple(aa), tuple(bb)

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9
    # Config.set('graphics', 'resizable', '0')
    # Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = get_color_from_hex('#ffffff')

    PaintApp().run()
