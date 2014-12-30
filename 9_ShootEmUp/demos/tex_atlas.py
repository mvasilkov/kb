from __future__ import division
from collections import namedtuple
import json

from kivy.app import App
from kivy.base import EventLoop
from kivy.core.image import Image
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget

# u0, v0: top left corner
# u1, v1: bottom right corner
# su: equals to 0.5 * width
# sv: equals to 0.5 * height
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


class GlslDemo(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'tex_atlas.glsl'

        fmt = (
            (b'vCenter',     2, 'float'),
            (b'vPosition',   2, 'float'),
            (b'vTexCoords0', 2, 'float'),
        )

        texture, uvmap = load_atlas('icons.atlas')

        a = uvmap['icon_clock']
        vertices = (
            128, 128, -a.su, -a.sv, a.u0, a.v1,
            128, 128,  a.su, -a.sv, a.u1, a.v1,
            128, 128,  a.su,  a.sv, a.u1, a.v0,
            128, 128, -a.su,  a.sv, a.u0, a.v0,
        )
        indices = (0, 1, 2, 2, 3, 0)

        b = uvmap['icon_paint']
        vertices += (
            256, 256, -b.su, -b.sv, b.u0, b.v1,
            256, 256,  b.su, -b.sv, b.u1, b.v1,
            256, 256,  b.su,  b.sv, b.u1, b.v0,
            256, 256, -b.su,  b.sv, b.u0, b.v0,
        )
        indices += (4, 5, 6, 6, 7, 4)

        with self.canvas:
            Mesh(fmt=fmt, mode='triangles',
                 vertices=vertices, indices=indices,
                 texture=texture)


class GlslApp(App):
    def build(self):
        EventLoop.ensure_window()
        return GlslDemo()

if __name__ == '__main__':
    GlslApp().run()
