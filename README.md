# Tetris-2048

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Dubomr/Tetris-2048)

Tetris-2048 is a challenging puzzle game that merges the classic block-stacking gameplay of Tetris with the number-merging mechanics of 2048. Control falling tetrominoes made of numbered tiles, and strategically place them to create higher numbers. The ultimate goal is to form the 2048 tile while clearing lines and maximizing your score.

## Features

- **Hybrid Gameplay:** Experience a novel blend of two beloved puzzle genres.
- **Merging Mechanics:** Combine adjacent tiles of the same number to double their value, similar to 2048.
- **Line Clearing:** Clear full horizontal lines to score points based on the sum of the tile values in the row.
- **Chain Reactions:** Clearing lines or merging tiles can cause floating blocks to fall, potentially triggering cascades of merges and line clears.
- **Dynamic Difficulty:** Game speed increases as your score goes up, challenging your reflexes and planning skills.
- **Swap Piece:** Swap the current falling tetromino with the next one to optimize your strategy (once per piece).
- **Scoring System:** Earn points from merging tiles, clearing full rows, and removing unlinked "floating" tiles.
- **Sound and Music:** Includes background music and sound effects for an immersive experience.

## How to Play

The objective is to merge tiles to create the 2048 tile without letting the blocks stack to the top of the grid.

### Controls

- **← Left Arrow:** Move piece to the left.
- **→ Right Arrow:** Move piece to the right.
- **↓ Down Arrow:** Soft drop the piece (move down one step).
- **↑ Up Arrow:** Rotate the piece.
- **Spacebar:** Hard drop the piece instantly to the bottom.
- **C:** Swap the current piece with the next piece.
- **P:** Pause or resume the game.
- **R:** Restart the game.

## Installation

This project requires Python and a few external libraries. The included sound module (`winsound`) is specific to the Windows operating system.

1.  Clone the repository to your local machine:

    ```sh
    git clone https://github.com/dubomr/tetris-2048.git
    cd tetris-2048
    ```

2.  Install the required Python packages:

    ```sh
    pip install pygame numpy
    ```

3.  Run the game:
    ```sh
    python Tetris_2048.py
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
