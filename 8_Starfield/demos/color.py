from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class GlslDemo(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'color.glsl'

        fmt = (
            (b'vPosition', 2, 'float'),
            (b'vColor', 3, 'float'),
        )

        indices = (0, 1, 2, 2, 3, 0)

        vertices = (
            0,   0,   0.463, 0.839, 1,
            255, 0,   0.831, 0.984, 0.474,
            255, 255, 1,     0.541, 0.847,
            0,   255, 1,     0.988, 0.474,
        )

        with self.canvas:
            Mesh(fmt=fmt, mode='triangles',
                 indices=indices, vertices=vertices)


class GlslApp(App):
    def build(self):
        EventLoop.ensure_window()
        return GlslDemo()

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '300')
    GlslApp().run()
