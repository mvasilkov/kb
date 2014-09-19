from __future__ import division

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window, Keyboard
from kivy.graphics import Color, BorderImage
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

spacing = 15

colors = (
    'eee4da', 'ede0c8', 'f2b179', 'f59563',
    'f67c5f', 'f65e3b', 'edcf72', 'edcc61',
    'edc850', 'edc53f', 'edc22e')

tile_colors = {2 ** (i + 1): colors[i]
               for i in range(len(colors))}

key_vectors = {
    Keyboard.keycodes['up']: (0, 1),
    Keyboard.keycodes['right']: (1, 0),
    Keyboard.keycodes['down']: (0, -1),
    Keyboard.keycodes['left']: (-1, 0),
}


class Tile(Widget):
    font_size = NumericProperty(24)
    number = NumericProperty(2)
    color = ListProperty(get_color_from_hex(tile_colors[2]))
    number_color = ListProperty(get_color_from_hex('776e65'))

    def __init__(self, number=2, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.font_size = 0.5 * self.width
        self.number = number
        self.color = get_color_from_hex(tile_colors[number])
        if self.number > 4:
            self.number_color = get_color_from_hex('f9f6f2')

    def resize(self, pos, size):
        self.pos = pos
        self.size = size
        self.font_size = 0.5 * self.width


def all_cells(flip_x=False, flip_y=False):
    for x in (range(3, -1, -1) if flip_x else range(4)):
        for y in (range(3, -1, -1) if flip_y else range(4)):
            yield (x, y)


class Board(Widget):
    b = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.resize()

    def reset(self):
        self.b = [[None for i in range(4)] for j in range(4)]
        Clock.schedule_once(self.new_tile, 0.1)

    def new_tile(self, *args):
        tile = Tile(pos=self.cell_pos(1, 1), size=self.cell_size)
        self.b[1][1] = tile
        self.add_widget(tile)

    def move(self, dir_x, dir_y):
        for board_x, board_y in all_cells(dir_x > 0, dir_y > 0):
            tile = self.b[board_x][board_y]
            if not tile:
                continue
            new_x, new_y = board_x, board_y
            while self.can_move(new_x + dir_x, new_y + dir_y):
                self.b[new_x][new_y] = None
                new_x += dir_x
                new_y += dir_y
                self.b[new_x][new_y] = tile
                tile.pos = self.cell_pos(new_x, new_y)

    def can_move(self, board_x, board_y):
        return (board_x >= 0 and board_y >= 0 and
                board_x <= 3 and board_y <= 3 and
                self.b[board_x][board_y] is None)

    def cell_pos(self, board_x, board_y):
        return (self.x + board_x * (self.cell_size[0] + spacing) + spacing,
                self.y + board_y * (self.cell_size[1] + spacing) + spacing)

    def resize(self, *args):
        self.cell_size = (0.25 * (self.width - 5 * spacing), ) * 2

        # redraw background
        self.canvas.before.clear()
        with self.canvas.before:
            BorderImage(pos=self.pos, size=self.size, source='board.png')
            Color(*get_color_from_hex('ccc0b4'))
            for board_x, board_y in all_cells():
                BorderImage(pos=self.cell_pos(board_x, board_y),
                            size=self.cell_size, source='cell.png')

        # resize tiles
        if not self.b:
            return
        for board_x, board_y in all_cells():
            tile = self.b[board_x][board_y]
            if tile:
                tile.resize(pos=self.cell_pos(board_x, board_y),
                            size=self.cell_size)

    on_pos = resize
    on_size = resize

    def on_key_down(self, window, key, *args):
        if key in key_vectors:
            self.move(*key_vectors[key])


class GameApp(App):
    def on_start(self):
        board = self.root.ids.board
        board.reset()
        Window.bind(on_key_down=board.on_key_down)


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    GameApp().run()
