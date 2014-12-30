import math
from random import random

from kivy import utils
from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Image
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget

NSTARS = 1000


class Star:
    angle = 0
    distance = 0
    size = 0.1

    def __init__(self, sf, i):
        self.sf = sf
        self.j = 4 * i * sf.vsize
        self.reset()

    def reset(self):
        self.angle = 2 * math.pi * random()
        self.distance = 90 * random() + 10
        self.size = 0.05 * random() + 0.05

    def iterate(self):
        return range(self.j,
                     self.j + 4 * self.sf.vsize,
                     self.sf.vsize)

    def update(self, x0, y0):
        x = x0 + self.distance * math.cos(self.angle)
        y = y0 + self.distance * math.sin(self.angle)

        for i in self.iterate():
            self.sf.vertices[i:i + 3] = (x, y, self.size)


class Starfield(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'starfield.glsl'

        self.vfmt = (
            (b'vCenter',     2, 'float'),
            (b'vScale',      1, 'float'),
            (b'vPosition',   2, 'float'),
            (b'vTexCoords0', 2, 'float'),
        )

        self.vsize = sum(attr[1] for attr in self.vfmt)

        self.indices = []
        for i in range(0, 4 * NSTARS, 4):
            self.indices.extend((
                i, i + 1, i + 2, i + 2, i + 3, i))

        self.vertices = []
        for i in range(NSTARS):
            self.vertices.extend((
                0, 0, 1, -24, -24, 0, 1,
                0, 0, 1,  24, -24, 1, 1,
                0, 0, 1,  24,  24, 1, 0,
                0, 0, 1, -24,  24, 0, 0,
            ))

        self.texture = Image('star.png').texture

        self.stars = [Star(self, i) for i in range(NSTARS)]

    def update_glsl(self, nap):
        x0, y0 = self.center
        max_distance = 1.1 * max(x0, y0)

        for star in self.stars:
            star.distance *= 2 * nap + 1
            star.size += 0.25 * nap

            if (star.distance > max_distance):
                star.reset()
            else:
                star.update(x0, y0)

        self.canvas.clear()

        with self.canvas:
            Mesh(fmt=self.vfmt, mode='triangles',
                 indices=self.indices, vertices=self.vertices,
                 texture=self.texture)


class StarfieldApp(App):
    def build(self):
        EventLoop.ensure_window()
        return Starfield()

    def on_start(self):
        Clock.schedule_interval(self.root.update_glsl, 60 ** -1)

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')
    Config.set('graphics', 'show_cursor', '0')
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = utils.get_color_from_hex('111110')

    StarfieldApp().run()
