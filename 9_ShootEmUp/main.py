from __future__ import division
from collections import namedtuple
import json
import math
from random import randint, random

from kivy import platform
from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '540')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'show_cursor', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.core.audio import SoundLoader
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
            (b'vCenter', 2, 'float'),
            (b'vScale', 1, 'float'),
            (b'vPosition', 2, 'float'),
            (b'vTexCoords0', 2, 'float'),
        )

        self.vsize = sum(attr[1] for attr in self.vfmt)

        self.texture, self.uvmap = load_atlas(self.atlas)

    def make_particles(self, Cls, num):
        count = len(self.particles)
        uv = self.uvmap[Cls.tex_name]

        for i in range(count, count + num):
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


class MultiAudio:
    _next = 0

    def __init__(self, filename, count):
        self.buf = [SoundLoader.load(filename)
                    for i in range(count)]

    def play(self):
        self.buf[self._next].play()
        self._next = (self._next + 1) % len(self.buf)

snd_hit = MultiAudio('hit.wav', 5)
snd_laser = MultiAudio('laser.wav', 10)


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
            self.size = random() + 0.6

    def advance(self, nap):
        self.size -= nap
        if self.size <= 0.1:
            self.reset()
        else:
            self.x -= 120 * nap


class Bullet(Particle):
    active = False
    tex_name = 'bullet'

    def reset(self, created=False):
        self.active = False
        self.x = -100
        self.y = -100

    def advance(self, nap):
        if self.active:
            self.x += 250 * nap
            if self.x > self.parent.width:
                self.reset()

        elif (self.parent.firing and
              self.parent.fire_delay <= 0):
            snd_laser.play()

            self.active = True
            self.x = self.parent.player_x + 40
            self.y = self.parent.player_y
            self.parent.fire_delay += 0.3333


class Enemy(Particle):
    active = False
    tex_name = 'ufo'
    v = 0

    def reset(self, created=False):
        self.active = False
        self.x = -100
        self.y = -100
        self.v = 0

    def advance(self, nap):
        if self.active:
            if self.check_hit():
                snd_hit.play()

                self.reset()
                return

            self.x -= 200 * nap
            if self.x < -50:
                self.reset()
                return

            self.y += self.v * nap
            if self.y <= 0:
                self.v = abs(self.v)
            elif self.y >= self.parent.height:
                self.v = -abs(self.v)

        elif self.parent.spawn_delay <= 0:
            self.active = True
            self.x = self.parent.width + 50
            self.y = self.parent.height * random()
            self.v = randint(-100, 100)
            self.parent.spawn_delay += 1

    def check_hit(self):
        if math.hypot(self.parent.player_x - self.x,
                      self.parent.player_y - self.y) < 60:
            return True

        for b in self.parent.bullets:
            if not b.active:
                continue

            if math.hypot(b.x - self.x, b.y - self.y) < 30:
                b.reset()
                return True


class Game(PSWidget):
    glsl = 'game.glsl'
    atlas = 'game.atlas'

    firing = False
    fire_delay = 0
    spawn_delay = 1

    use_mouse = platform not in ('ios', 'android')

    def initialize(self):
        self.player_x, self.player_y = self.center

        self.make_particles(Star, 200)
        self.make_particles(Trail, 200)
        self.make_particles(Player, 1)
        self.make_particles(Enemy, 25)
        self.make_particles(Bullet, 25)

        self.bullets = self.particles[-25:]

    def update_glsl(self, nap):
        if self.use_mouse:
            self.player_x, self.player_y = Window.mouse_pos

        if self.firing:
            self.fire_delay -= nap

        self.spawn_delay -= nap

        PSWidget.update_glsl(self, nap)

    def on_touch_down(self, touch):
        self.player_x, self.player_y = touch.pos
        self.firing = True
        self.fire_delay = 0

    def on_touch_move(self, touch):
        self.player_x, self.player_y = touch.pos

    def on_touch_up(self, touch):
        self.firing = False


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
