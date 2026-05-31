import lib.stddraw as stddraw
from lib.color import Color
import random

# A class for modeling numbered tiles as in 2048
class Tile:
    boundary_thickness = 0.004
    font_family, font_size = 'Arial', 16

    def __init__(self, number=None):
        if number is None:
            self.number = random.choice([2, 4])
        else:
            self.number = number

        self.update_colors()

    def update_colors(self):
        color_map = {
            2:   (238, 228, 218),
            4:   (237, 224, 200),
            8:   (242, 177, 121),
            16:  (245, 149, 99),
            32:  (246, 124, 95),
            64:  (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }

        bg = color_map.get(self.number, (60, 58, 50))
        self.background_color = Color(*bg)

        if self.number <= 4:
            self.foreground_color = Color(119, 110, 101)
        else:
            self.foreground_color = Color(249, 246, 242)

        self.box_color = Color(187, 173, 160)

    def set_number(self, number):
        self.number = number
        self.update_colors()

    def draw(self, position, length=1):
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)

        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()

        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.boldText(position.x, position.y, str(self.number))
