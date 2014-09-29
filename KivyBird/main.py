from __future__ import division

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


class Background(Widget):
    floor = ObjectProperty(None)
    green = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.floor = Image('floor.png').texture
        self.green = Image('green.png').texture
        self.floor.wrap = self.green.wrap = 'repeat'
        self.on_size()
        Clock.schedule_interval(self.update, 0.016)

    def on_size(self, *args):
        self.floor.uvsize = (self.width / self.floor.width, -1)
        self.green.uvsize = (self.width / self.green.width, -1)

    def update(self, nap):
        self.floor.uvpos = (
            self.floor.uvpos[0] + 2 * nap, self.floor.uvpos[1])
        self.green.uvpos = (
            self.green.uvpos[0] + 0.5 * nap, self.green.uvpos[1])
        self.property('floor').dispatch(self)
        self.property('green').dispatch(self)


class KivyBirdApp(App):
    pass

if __name__ == '__main__':
    KivyBirdApp().run()
