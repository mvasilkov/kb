from __future__ import division
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image
from kivy.core.window import Window, Keyboard
from kivy.properties import (AliasProperty,
                             ListProperty,
                             NumericProperty,
                             ObjectProperty)
from kivy.uix.image import Image as ImageWidget
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class MultiAudio:
    _next = 0

    def __init__(self, filename, count):
        self.buf = [SoundLoader.load(filename)
                    for i in range(count)]

    def play(self):
        self.buf[self._next].play()
        self._next = (self._next + 1) % len(self.buf)

snd_bump = MultiAudio('bump.wav', 4)
snd_game_over = SoundLoader.load('game_over.wav')


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

    upper_y = AliasProperty(
        lambda self: self.height - self.upper_len,
        None, bind=['height', 'upper_len'])

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


class Bird(ImageWidget):
    ACCEL_JUMP = 5
    ACCEL_FALL = 0.25

    speed = NumericProperty(0)
    angle = AliasProperty(
        lambda self: 5 * self.speed,
        None, bind=['speed'])

    def __init__(self, **kwargs):
        super(Bird, self).__init__(**kwargs)

    def gravity_on(self, height):
        # Replace pos_hint with a value
        self.pos_hint.pop('center_y', None)
        self.center_y = 0.6 * height

    def bump(self):
        self.speed = Bird.ACCEL_JUMP

    def update(self, nap):
        self.speed -= Bird.ACCEL_FALL
        self.y += self.speed


class KivyBirdApp(App):
    playing = False
    pipes = []

    def on_start(self):
        self.spacing = 0.5 * self.root.width

        self.background = self.root.ids.background
        self.bird = self.root.ids.bird
        Clock.schedule_interval(self.update, 0.016)

        Window.bind(on_key_down=self.on_key_down)
        self.background.on_touch_down = self.user_action

    def spawn_pipes(self):
        for p in self.pipes:
            self.root.remove_widget(p)

        self.pipes = []

        for i in range(4):
            p = Pipe(x=self.root.width + (self.spacing * i))
            p.ratio = random.uniform(0.25, 0.75)
            self.root.add_widget(p)
            self.pipes.append(p)

    def update(self, nap):
        self.background.update(nap)
        if not self.playing:
            return  # don't move bird or pipes

        self.bird.update(nap)

        for p in self.pipes:
            p.x -= 96 * nap
            if p.x <= -64:  # pipe gone off screen
                p.x += 4 * self.spacing
                p.ratio = random.uniform(0.25, 0.75)

        if self.test_game_over():
            snd_game_over.play()
            self.playing = False

    def on_key_down(self, window, key, *args):
        if key == Keyboard.keycodes['spacebar']:
            self.user_action()

    def user_action(self, *args):
        snd_bump.play()

        if not self.playing:
            self.bird.gravity_on(self.root.height)
            self.spawn_pipes()
            self.playing = True

        self.bird.bump()

    def test_game_over(self):
        screen_height = self.root.height

        if self.bird.y < 90 or \
                self.bird.y > screen_height - 50:
            return True

        for p in self.pipes:
            if not p.collide_widget(self.bird):
                continue

            if (self.bird.y < p.lower_len + 116 or
                self.bird.y > screen_height - (
                    p.upper_len + 75)):
                return True

        return False

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('00bfff')
    KivyBirdApp().run()
