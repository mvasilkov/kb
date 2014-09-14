from __future__ import division

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import AliasProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

SPACING = 15


class Game2048Board(Widget):
    def get_cell_size(self):
        size = 0.25 * (self.width - 5 * SPACING)
        return (size, size)

    def get_cell_pos(self):
        size = self.get_cell_size()
        return [[(self.x + SPACING + board_x * (size[0] + SPACING),
                  self.y + SPACING + board_y * (size[1] + SPACING))
                 for board_y in range(0, 4)]
                for board_x in range(0, 4)]

    cell_size = AliasProperty(get_cell_size, None, bind=['width'])
    cell_pos = AliasProperty(get_cell_pos, None, bind=['cell_size'])


class Game2048App(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    Game2048App().run()
