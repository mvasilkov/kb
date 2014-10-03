from __future__ import division
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.properties import (ListProperty,
                             NumericProperty,
                             ObjectProperty)
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class BaseWidget(Widget):
    def load_tileable(self, name):
        t = Image('%s.png' % name).texture
        t.wrap = 'repeat'
        setattr(self, 'tx_%s' % name, t)


class Background(BaseWidget):
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

    def on_size(self, *args):
        for t in (self.tx_floor, self.tx_grass, self.tx_cloud):
            self.set_background_size(t)

    def update(self, nap):
        self.set_background_uv('tx_floor', 2 * nap)
        self.set_background_uv('tx_grass', 0.5 * nap)
        self.set_background_uv('tx_cloud', 0.1 * nap)


class Pipe(BaseWidget):
    FLOOR = 96
    PCAP_HEIGHT = 26
    PIPE_GAP = 120

    tx_pipe = ObjectProperty(None)
    tx_pcap = ObjectProperty(None)

    ratio = NumericProperty(0.5)
    lower_len = NumericProperty(0)
    lower_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    upper_len = NumericProperty(0)
    upper_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    upper_y = NumericProperty(0)

    def set_coords(self, coords, len):
        len /= 16  # height of texture
        coords[5:] = (len, 0, len)

    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)

        for name in 'pipe pcap'.split():
            self.load_tileable(name)

        self.bind(ratio=self.on_size)

    def on_size(self, *args):
        pipes_length = self.height - (
            Pipe.FLOOR + Pipe.PIPE_GAP + 2 * Pipe.PCAP_HEIGHT)
        self.lower_len = self.ratio * pipes_length
        self.upper_len = pipes_length - self.lower_len
        self.set_coords(self.lower_coords, self.lower_len)
        self.set_coords(self.upper_coords, self.upper_len)
        self.upper_y = self.height - self.upper_len


class KivyBirdApp(App):
    pipes = []

    def on_start(self):
        self.spacing = 0.5 * self.root.width
        self.spawn_pipes()

        self.background = self.root.ids.background
        Clock.schedule_interval(self.update, 0.016)

    def spawn_pipes(self):
        for p in self.pipes:
            self.root.remove_widget(p)

        for i in range(4):
            p = Pipe(x=self.root.width + (self.spacing * i))
            p.ratio = random.uniform(0.25, 0.75)
            self.root.add_widget(p)
            self.pipes.append(p)

        self.root.canvas.ask_update()

    def update(self, nap):
        self.background.update(nap)
        for p in self.pipes:
            p.x -= 96 * nap
            if p.x <= -64:  # gone off screen
                p.x += 4 * self.spacing
                p.ratio = random.uniform(0.25, 0.75)


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('00bfff')
    KivyBirdApp().run()
