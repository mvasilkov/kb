from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.core.image import Image
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class GlslDemo(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'tex_image.glsl'

        fmt = (
            (b'vPosition', 2, 'float'),
            (b'vTexCoords0', 2, 'float'),
        )

        indices = (0, 1, 2, 2, 3, 0)

        vertices = (
            0,   0,   0, 1,
            255, 0,   1, 1,
            255, 255, 1, 0,
            0,   255, 0, 0,
        )

        with self.canvas:
            Mesh(fmt=fmt, mode='triangles',
                 indices=indices, vertices=vertices,
                 texture=Image('kivy.png').texture)


class GlslApp(App):
    def build(self):
        EventLoop.ensure_window()
        return GlslDemo()

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '300')
    GlslApp().run()
