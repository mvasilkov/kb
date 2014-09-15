from __future__ import division

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, BorderImage
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

spacing = 15


def all_cells():
    for x in range(0, 4):
        for y in range(0, 4):
            yield (x, y)


class Game2048Board(Widget):
    def __init__(self, **kwargs):
        super(Game2048Board, self).__init__(**kwargs)
        self.refresh()

    def cell_pos(self, board_x, board_y):
        return (self.x + board_x * (self.cell_size[0] + spacing) + spacing,
                self.y + board_y * (self.cell_size[1] + spacing) + spacing)

    def refresh(self, *args):
        self.cell_size = (0.25 * (self.width - 5 * spacing), ) * 2
        self.canvas.before.clear()
        with self.canvas.before:
            BorderImage(pos=self.pos, size=self.size, source='board.png')
            Color(*get_color_from_hex('ccc0b4'))
            for board_x, board_y in all_cells():
                BorderImage(pos=self.cell_pos(board_x, board_y),
                            size=self.cell_size, source='cell.png')

    on_pos = refresh
    on_size = refresh


class Game2048App(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    Game2048App().run()
