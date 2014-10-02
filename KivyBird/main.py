from __future__ import division

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.properties import (ListProperty,
                             NumericProperty,
                             ObjectProperty)
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class TxWidget(Widget):
    def load_tileable(self, name):
        t = Image('%s.png' % name).texture
        t.wrap = 'repeat'
        setattr(self, 'tx_%s' % name, t)


class Background(TxWidget):
    tx_floor = ObjectProperty(None)
    tx_grass = ObjectProperty(None)
    tx_cloud = ObjectProperty(None)

    def set_background_size(self, t):
        t.uvsize = (self.width / t.width, -1)

    def set_background_uv(self, name, val):
        t = getattr(self, name)
        t.uvpos = ((t.uvpos[0] + val) % self.width, t.uvpos[1])
        self.property(name).dispatch(self)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)

        for name in 'floor grass cloud'.split():
            self.load_tileable(name)

        self.on_size()
        Clock.schedule_interval(self.update, 0.016)

    def on_size(self, *args):
        for t in (self.tx_floor, self.tx_grass, self.tx_cloud):
            self.set_background_size(t)

    def update(self, nap):
        self.set_background_uv('tx_floor', 2 * nap)
        self.set_background_uv('tx_grass', 0.5 * nap)
        self.set_background_uv('tx_cloud', 0.1 * nap)


class Pipe(TxWidget):
    FLOOR = 96
    PCAP_HEIGHT = 26
    PIPE_GAP = 120

    tx_pipe = ObjectProperty(None)
    tx_pcap = ObjectProperty(None)

    lower_len = NumericProperty(0)
    lower_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    upper_len = NumericProperty(0)
    upper_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    upper_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)

        for name in 'pipe pcap'.split():
            self.load_tileable(name)

        self.on_size()

    def on_size(self, *args):
        pipes_length = self.height - (
            Pipe.FLOOR + Pipe.PIPE_GAP + 2 * Pipe.PCAP_HEIGHT)
        self.lower_len = self.upper_len = 0.5 * pipes_length
        self.lower_coords[5] = self.lower_coords[7] = self.lower_len / 16
        self.upper_coords[5] = self.upper_coords[7] = self.upper_len / 16
        self.upper_y = self.height - self.upper_len


class KivyBirdApp(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#00bfff')
    KivyBirdApp().run()
