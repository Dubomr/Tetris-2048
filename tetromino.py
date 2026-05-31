from tile import Tile
from point import Point
import copy as cp
import random
import numpy as np
import winsound

class Tetromino:
    SHAPES = {
        'I': [(1,0), (1,1), (1,2), (1,3)],
        'J': [(0,0), (1,0), (1,1), (1,2)],
        'L': [(1,0), (1,1), (1,2), (2,0)],
        'O': [(0,0), (0,1), (1,0), (1,1)],
        'S': [(0,1), (1,1), (1,2), (2,2)],
        'T': [(0,1), (1,0), (1,1), (1,2)],
        'Z': [(0,2), (1,2), (1,1), (2,1)]
    }

    grid_height, grid_width = None, None

    def __init__(self, type):
        self.type = type

        if self.type == 'I':
            n = 4
        elif self.type == 'O':
            n = 2
        else:
            n = 3

        self.tile_matrix = np.full((n, n), None)

        for i in range(4):
            col_index, row_index = self.SHAPES[type][i][0], self.SHAPES[type][i][1]
            self.tile_matrix[row_index][col_index] = Tile()

        self.bottom_left_cell = Point()
        self.reset_position()

    def reset_position(self):
        n = len(self.tile_matrix)
        self.bottom_left_cell.y = Tetromino.grid_height - 1
        self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

    def get_cell_position(self, row, col):
        n = len(self.tile_matrix)
        position = Point()
        position.x = self.bottom_left_cell.x + col
        position.y = self.bottom_left_cell.y + (n - 1) - row
        return position

    def get_min_bounded_tile_matrix(self, return_position=False):
        n = len(self.tile_matrix)
        min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0

        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    if row < min_row:
                        min_row = row
                    if row > max_row:
                        max_row = row
                    if col < min_col:
                        min_col = col
                    if col > max_col:
                        max_col = col

        copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if self.tile_matrix[row][col] is not None:
                    row_ind = row - min_row
                    col_ind = col - min_col
                    copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])

        if not return_position:
            return copy
        else:
            blc_position = cp.copy(self.bottom_left_cell)
            blc_position.translate(min_col, (n - 1) - max_row)
            return copy, blc_position

    def draw(self):
        n = len(self.tile_matrix)
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    position = self.get_cell_position(row, col)
                    if position.y < Tetromino.grid_height:
                        self.tile_matrix[row][col].draw(position)

    def move(self, direction, game_grid):
        if not self.can_be_moved(direction, game_grid):
            return False

        if direction == 'left':
            self.bottom_left_cell.x -= 1
        elif direction == 'right':
            self.bottom_left_cell.x += 1
        else:
            self.bottom_left_cell.y -= 1
        return True

    def rotate(self, game_grid):
        if self.type == 'O':
            return True

        old_matrix = cp.deepcopy(self.tile_matrix)
        self.tile_matrix = np.rot90(self.tile_matrix, k=-1)

        if not self.can_be_rotated(game_grid):
            self.tile_matrix = old_matrix
            return False
        
        winsound.PlaySound("sounds/rotate.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)

        return True

    def can_be_rotated(self, game_grid):
        n = len(self.tile_matrix)
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    pos = self.get_cell_position(row, col)
                    if not game_grid.is_inside(pos.y, pos.x) or game_grid.is_occupied(pos.y, pos.x):
                        return False
        return True

    def hard_drop(self, game_grid):
        steps = 0
        while self.move('down', game_grid):
            steps += 1
        
        winsound.PlaySound("sounds/harddrop.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        return steps

    def draw_at_position(self, position):
        n = len(self.tile_matrix)
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    draw_pos = Point()
                    draw_pos.x = position.x + col
                    draw_pos.y = position.y + (n - 1 - row)
                    self.tile_matrix[row][col].draw(draw_pos)

    def can_be_moved(self, direction, game_grid):
        n = len(self.tile_matrix)

        if direction == 'left' or direction == 'right':
            for row_index in range(n):
                for col_index in range(n):
                    row, col = row_index, col_index
                    if direction == 'left' and self.tile_matrix[row][col] is not None:
                        leftmost = self.get_cell_position(row, col)
                        if leftmost.x == 0:
                            return False
                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False
                        break

                    row, col = row_index, n - 1 - col_index
                    if direction == 'right' and self.tile_matrix[row][col] is not None:
                        rightmost = self.get_cell_position(row, col)
                        if rightmost.x == Tetromino.grid_width - 1:
                            return False
                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False
                        break
        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    if self.tile_matrix[row][col] is not None:
                        bottommost = self.get_cell_position(row, col)
                        if bottommost.y == 0:
                            return False
                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False
                        break

        return True
