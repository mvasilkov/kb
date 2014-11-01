from __future__ import division
from collections import namedtuple
import json
from random import randint, random

from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '540')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'show_cursor', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

UVMapping = namedtuple('UVMapping', 'u0 v0 u1 v1 su sv')


def load_atlas(atlas_name):
    with open(atlas_name, 'rb') as f:
        atlas = json.loads(f.read().decode('utf-8'))

    tex_name, mapping = atlas.popitem()
    tex = Image(tex_name).texture
    tex_width, tex_height = tex.size

    uvmap = {}
    for name, val in mapping.items():
        x0, y0, w, h = val
        x1, y1 = x0 + w, y0 + h
        uvmap[name] = UVMapping(
            x0 / tex_width, 1 - y1 / tex_height,
            x1 / tex_width, 1 - y0 / tex_height,
            0.5 * w, 0.5 * h)

    return tex, uvmap


class Particle:
    x = 0
    y = 0
    size = 1

    def __init__(self, parent, i):
        self.parent = parent
        self.vsize = parent.vsize
        self.base_i = 4 * i * self.vsize
        self.reset(created=True)

    def update(self):
        for i in range(self.base_i,
                       self.base_i + 4 * self.vsize,
                       self.vsize):
            self.parent.vertices[i:i + 3] = (
                self.x, self.y, self.size)

    def reset(self, created=False):
        raise NotImplementedError()

    def advance(self, nap):
        raise NotImplementedError()


class PSWidget(Widget):
    indices = []
    vertices = []
    particles = []

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = self.glsl

        self.vfmt = (
            ('vCenter', 2, 'float'),
            ('vScale', 1, 'float'),
            ('vPosition', 2, 'float'),
            ('vTexCoords0', 2, 'float'),
        )

        self.vsize = sum(attr[1] for attr in self.vfmt)

        self.texture, self.uvmap = load_atlas(self.atlas)

    def make_particles(self, Cls, num):
        count = len(self.particles)
        uv = self.uvmap[Cls.tex_name]

        for i in xrange(count, count + num):
            j = 4 * i
            self.indices.extend((
                j, j + 1, j + 2, j + 2, j + 3, j))

            self.vertices.extend((
                0, 0, 1, -uv.su, -uv.sv, uv.u0, uv.v1,
                0, 0, 1,  uv.su, -uv.sv, uv.u1, uv.v1,
                0, 0, 1,  uv.su,  uv.sv, uv.u1, uv.v0,
                0, 0, 1, -uv.su,  uv.sv, uv.u0, uv.v0,
            ))

            p = Cls(self, i)
            self.particles.append(p)

    def update_glsl(self, nap):
        for p in self.particles:
            p.advance(nap)
            p.update()

        self.canvas.clear()

        with self.canvas:
            Mesh(fmt=self.vfmt, mode='triangles',
                 indices=self.indices, vertices=self.vertices,
                 texture=self.texture)


class Star(Particle):
    plane = 1
    tex_name = 'star'

    def reset(self, created=False):
        self.plane = randint(1, 3)

        if created:
            self.x = random() * self.parent.width
        else:
            self.x = self.parent.width

        self.y = random() * self.parent.height
        self.size = 0.1 * self.plane

    def advance(self, nap):
        self.x -= 20 * self.plane * nap
        if self.x < 0:
            self.reset()


class Player(Particle):
    tex_name = 'player'

    def reset(self, created=False):
        self.x = self.parent.player_x
        self.y = self.parent.player_y

    advance = reset


class Trail(Particle):
    tex_name = 'trail'

    def reset(self, created=False):
        self.x = self.parent.player_x + randint(-30, -20)
        self.y = self.parent.player_y + randint(-10, 10)

        if created:
            self.size = 0
        else:
            self.size = 1.5 * random() + 0.1

    def advance(self, nap):
        self.size -= nap
        if self.size <= 0.1:
            self.reset()
        else:
            self.x -= 120 * nap


class Game(PSWidget):
    glsl = 'game.glsl'
    atlas = 'game.atlas'

    def initialize(self):
        self.player_x, self.player_y = self.center

        self.make_particles(Star, 200)
        self.make_particles(Trail, 300)
        self.make_particles(Player, 1)

    def update_glsl(self, nap):
        self.player_x, self.player_y = Window.mouse_pos

        PSWidget.update_glsl(self, nap)


class GameApp(App):
    def build(self):
        EventLoop.ensure_window()
        return Game()

    def on_start(self):
        self.root.initialize()
        Clock.schedule_interval(self.root.update_glsl, 60 ** -1)

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('111110')

    GameApp().run()
