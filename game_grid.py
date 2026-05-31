import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np
from collections import deque
import winsound

# A class for modeling the game grid
class GameGrid:
    # A constructor that creates the game grid using the given dimensions
    def __init__(self, grid_h, grid_w):
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.current_tetromino = None
        self.game_over = False
        self.won = False

        self.empty_cell_color = Color(42, 69, 99)
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        self.line_thickness = 0.002
        self.box_thickness = 5 * self.line_thickness

    # A method for displaying the game grid
    def display(self):
        stddraw.clear(self.empty_cell_color)
        self.draw_grid()
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        self.draw_boundaries()

    # A method for drawing the grid
    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))

        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)

        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5

        for x in np.arange(start_x + 1, end_x, 1):
            stddraw.line(x, start_y, x, end_y)

        for y in np.arange(start_y + 1, end_y, 1):
            stddraw.line(start_x, y, end_x, y)

        stddraw.setPenRadius()

    # Draw boundaries
    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.rectangle(-0.5, -0.5, self.grid_width, self.grid_height)
        stddraw.setPenRadius()

    # Check occupancy
    def is_occupied(self, row, col):
        if not self.is_inside(row, col):
            return False
        return self.tile_matrix[row][col] is not None

    # Check bounds
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Lock tetromino and update grid
    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino = None
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])

        for col in range(n_cols):
            for row in range(n_rows):
                if tiles_to_lock[row][col] is not None:
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row

                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    else:
                        self.game_over = True

        return self.game_over

    # Collects all the tiles in each column.
    def collapse_columns(self):
        for col in range(self.grid_width):
            existing_tiles = []
            for row in range(self.grid_height):
                if self.tile_matrix[row][col] is not None:
                    existing_tiles.append(self.tile_matrix[row][col])

            for row in range(self.grid_height):
                if row < len(existing_tiles):
                    self.tile_matrix[row][col] = existing_tiles[row]
                else:
                    self.tile_matrix[row][col] = None

    # Bottom-to-top chain merge
    def merge_tiles(self):
        merge_score = 0
        merged_any = False

        while True:
            merged_in_this_pass = False

            for col in range(self.grid_width):
                row = 0
                while row < self.grid_height - 1:
                    bottom_tile = self.tile_matrix[row][col]
                    top_tile = self.tile_matrix[row + 1][col]

                    if bottom_tile is not None and top_tile is not None:
                        if bottom_tile.number == top_tile.number:
                            new_value = bottom_tile.number * 2
                            bottom_tile.set_number(new_value)
                            self.tile_matrix[row + 1][col] = None
                            merge_score += new_value
                            merged_in_this_pass = True
                            merged_any = True

                            winsound.PlaySound("sounds/merge.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)

                            if new_value == 2048:
                                self.won = True

                    row += 1

            if merged_in_this_pass:
                self.collapse_columns()
            else:
                break

        return merge_score, merged_any

    # Delete the entire row and add the sum of the numbers to the score.
    def clear_full_rows_and_score(self):
        row_score = 0
        row = 0

        while row < self.grid_height:
            is_full = True
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is None:
                    is_full = False
                    break

            if is_full:
                winsound.PlaySound("sounds/clear.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)


                for col in range(self.grid_width):
                    row_score += self.tile_matrix[row][col].number

                for r in range(row, self.grid_height - 1):
                    for c in range(self.grid_width):
                        self.tile_matrix[r][c] = self.tile_matrix[r + 1][c]

                for c in range(self.grid_width):
                    self.tile_matrix[self.grid_height - 1][c] = None
            else:
                row += 1

        return row_score

    # Find the 4-connected tiles at the bottom.
    def mark_connected_tiles(self):
        visited = np.full((self.grid_height, self.grid_width), False)
        q = deque()

        # Start with the filled cells in the base row.
        for col in range(self.grid_width):
            if self.tile_matrix[0][col] is not None:
                visited[0][col] = True
                q.append((0, col))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while q:
            row, col = q.popleft()
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if self.is_inside(nr, nc):
                    if not visited[nr][nc] and self.tile_matrix[nr][nc] is not None:
                        visited[nr][nc] = True
                        q.append((nr, nc))

        return visited

    # Remove unlinked tiles and add their values ​​to the score.
    def delete_free_tiles_and_update_score(self):
        connected = self.mark_connected_tiles()
        free_tile_score = 0

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None and not connected[row][col]:
                    free_tile_score += self.tile_matrix[row][col].number
                    self.tile_matrix[row][col] = None

        if free_tile_score > 0:
            self.collapse_columns()

        return free_tile_score

    # All procedures after tetromino down
    def process_after_landing(self):
        total_score = 0

        while True:
            step_changed = False

            merge_score, merged_any = self.merge_tiles()
            if merged_any:
                total_score += merge_score
                step_changed = True

            row_score = self.clear_full_rows_and_score()
            if row_score > 0:
                total_score += row_score
                step_changed = True

            free_tile_score = self.delete_free_tiles_and_update_score()
            if free_tile_score > 0:
                total_score += free_tile_score
                step_changed = True

            if not step_changed:
                break

        return total_score

    def draw_panel(self, score, next_tetromino, level):
        panel_start_x = self.grid_width - 0.5
        panel_w = 4

        stddraw.setPenColor(Color(170, 160, 150))
        stddraw.filledRectangle(panel_start_x, -0.5, panel_w, self.grid_height)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(24)
        stddraw.boldText(panel_start_x + panel_w / 2, self.grid_height - 2, "SCORE")
        stddraw.text(panel_start_x + panel_w / 2, self.grid_height - 4, str(score))

        stddraw.boldText(panel_start_x + panel_w / 2, self.grid_height - 8, "LEVEL")
        stddraw.text(panel_start_x + panel_w / 2, self.grid_height - 10, str(level))

        stddraw.boldText(panel_start_x + panel_w / 2, 6, "NEXT")

        if next_tetromino:
            next_pos = Point()
            next_pos.x = panel_start_x + 1
            next_pos.y = 2
            next_tetromino.draw_at_position(next_pos)


        stddraw.setFontSize(12)
        stddraw.text(panel_start_x + panel_w / 2, self.grid_height - 11, "P : Pause")
        stddraw.text(panel_start_x + panel_w / 2, self.grid_height - 12, "R : Restart")
        stddraw.text(panel_start_x + panel_w / 2, self.grid_height - 13, "C : Swap")
