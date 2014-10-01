from __future__ import division

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class Background(Widget):
    tx_floor = ObjectProperty(None)
    tx_green = ObjectProperty(None)
    tx_cloud = ObjectProperty(None)

    # --- helper functions ---

    def load_tileable(self, name):
        t = Image('%s.png' % name).texture
        t.wrap = 'repeat'
        setattr(self, 'tx_%s' % name, t)

    def set_background_size(self, t):
        t.uvsize = (self.width / t.width, -1)

    def set_background_uv(self, name, val):
        t = getattr(self, name)
        t.uvpos = ((t.uvpos[0] + val) % self.width, t.uvpos[1])
        self.property(name).dispatch(self)

    # --- end helper functions ---

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)

        for name in 'floor green cloud'.split():
            self.load_tileable(name)

        self.on_size()
        Clock.schedule_interval(self.update, 0.016)

    def on_size(self, *args):
        for t in (self.tx_floor, self.tx_green, self.tx_cloud):
            self.set_background_size(t)

    def update(self, nap):
        self.set_background_uv('tx_floor', 2 * nap)
        self.set_background_uv('tx_green', 0.5 * nap)
        self.set_background_uv('tx_cloud', 0.1 * nap)


class KivyBirdApp(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#00bfff')
    KivyBirdApp().run()
