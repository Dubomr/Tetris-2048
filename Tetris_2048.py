################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################


import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
import os
from game_grid import GameGrid
from tetromino import Tetromino
import random
import winsound


def main():
    grid_height, grid_width = 20, 12
    panel_width = 4
    total_width = grid_width + panel_width

    winsound.PlaySound("sounds/bgm.wav", winsound.SND_ASYNC | winsound.SND_NODEFAULT)

    stddraw.setCanvasSize(40 * total_width, 40 * grid_height)
    stddraw.setXscale(-0.5, total_width - 0.5)
    stddraw.setYscale(-0.5, grid_height - 0.5)

    Tetromino.grid_height = grid_height
    Tetromino.grid_width = grid_width

    display_game_menu(grid_height, total_width)

    while True:
        action = run_game(grid_height, grid_width, total_width)

        if action == "restart":
            continue
        elif action == "quit":
            break


def run_game(grid_height, grid_width, total_width):
    grid = GameGrid(grid_height, grid_width)

    score = 0
    level = 1
    base_speed = 500
    paused = False

    # Only one swap per dropped stone.
    swap_used_this_turn = False

    next_tetromino = create_tetromino()
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino

    while True:
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()

            if key_typed == 'p':
                paused = not paused

            elif key_typed == 'r':
                stddraw.clearKeysTyped()
                return "restart"

            elif not paused:
                if key_typed == 'left':
                    current_tetromino.move('left', grid)
                    winsound.PlaySound("sounds/move.wav", winsound.SND_ASYNC | winsound.SND_NODEFAULT)

                elif key_typed == 'right':
                    current_tetromino.move('right', grid)
                    winsound.PlaySound("sounds/move.wav", winsound.SND_ASYNC | winsound.SND_NODEFAULT)

                elif key_typed == 'down':
                    current_tetromino.move('down', grid)
                    winsound.PlaySound("sounds/move.wav", winsound.SND_ASYNC | winsound.SND_NODEFAULT)

                elif key_typed == 'up':
                    current_tetromino.rotate(grid)

                elif key_typed == 'space':
                    current_tetromino.hard_drop(grid)

                elif key_typed == 'c':
                    if not swap_used_this_turn:
                        current_tetromino, next_tetromino = next_tetromino, current_tetromino
                        current_tetromino.reset_position()
                        grid.current_tetromino = current_tetromino
                        swap_used_this_turn = True

                        winsound.PlaySound("sounds/swap.wav", winsound.SND_ASYNC | winsound.SND_NODEFAULT)
                elif key_typed=='l':
                    return show_end_screen("GAME OVER",score,total_width,grid_height)
                elif key_typed=='w':
                    return show_end_screen("YOU WIN!",score,total_width,grid_height)
                
            stddraw.clearKeysTyped()

        level = (score // 1024) + 1
        current_speed = max(50, base_speed - (level - 1) * 30)

        if not paused:
            success = current_tetromino.move('down', grid)

            if not success:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over = grid.update_grid(tiles, pos)

                score += grid.process_after_landing()

                if game_over:
                    return show_end_screen("GAME OVER", score, total_width, grid_height)

                if grid.won:
                    return show_end_screen("YOU WIN!", score, total_width, grid_height)

                current_tetromino = next_tetromino
                next_tetromino = create_tetromino()
                grid.current_tetromino = current_tetromino

                # The swap right is renewed because a new stone has arrived.
                swap_used_this_turn = False

        grid.display()
        grid.draw_panel(score, next_tetromino, level)

        if paused:
            draw_pause_text(grid_width, grid_height)

        stddraw.show(current_speed if not paused else 100)


def create_tetromino():
    tetromino_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    return Tetromino(random_type)


def display_game_menu(grid_height, total_width):
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)

    stddraw.clear(background_color)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = os.path.join(current_dir, 'images/menu_image.png')

    img_center_x, img_center_y = (total_width - 1) / 2, grid_height - 7
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    button_w, button_h = total_width - 1.5, 2
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    stddraw.setFontFamily('Arial')
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    stddraw.text(img_center_x, 5, 'Click Here to Start the Game')

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w:
                if button_blc_y <= mouse_y <= button_blc_y + button_h:
                    break


def draw_pause_text(grid_width, grid_height):
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.setFontSize(30)
    stddraw.boldText(grid_width / 2, grid_height / 2, "PAUSED")
    stddraw.setFontSize(16)
    stddraw.text(grid_width / 2, grid_height / 2 - 1.5, "Press P to continue")


def show_end_screen(message, score, total_width, grid_height):

    if message=="GAME OVER":
        winsound.PlaySound("sounds/gameover.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    elif message=="YOU WIN!":
        winsound.PlaySound("sounds/win.wav",winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    while True:
        stddraw.clear(Color(42, 69, 99))
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontSize(32)
        stddraw.boldText((total_width - 1) / 2, grid_height / 2 + 2, message)

        stddraw.setFontSize(20)
        stddraw.text((total_width - 1) / 2, grid_height / 2, f"Score: {score}")
        stddraw.text((total_width - 1) / 2, grid_height / 2 - 2, "Press R to Restart")
        stddraw.text((total_width - 1) / 2, grid_height / 2 - 3, "Press Q to Quit")
        stddraw.show(100)

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            stddraw.clearKeysTyped()

            if key == 'r':
                return "restart"
            elif key == 'q':
                return "quit"


main()
