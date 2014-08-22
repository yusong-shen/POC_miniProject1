"""
2048 GUI
"""

import simplegui
import codeskulptor
import math

# Tile Images
IMAGENAME = "assets_2048.png"
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class GUI:
    """
    Class to run game GUI.
    """
    
    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._frame = simplegui.create_frame('2048', 
                        self._cols * TILE_SIZE + 2 * BORDER_SIZE, 
                        self._rows * TILE_SIZE + 2 * BORDER_SIZE)
        self._frame.add_button('New Game', self.start)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_canvas_background("#A39480")
        self._frame.start()
        self._game = game
        url = codeskulptor.file2url(IMAGENAME)
        self._tiles = simplegui.load_image(url)
        self._directions = {"up": UP, "down": DOWN, 
                            "left": LEFT, "right": RIGHT}
        
        
    def keydown(self, key):
        """
        Keydown handler
        """
        for dirstr, dirval in self._directions.items():
            if key == simplegui.KEY_MAP[dirstr]:
                self._game.move(dirval)
                break
        
    def draw(self, canvas):
        """
        Draw handler
        """
        for row in range(self._rows):
            for col in range(self._cols):               
                tile = self._game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                canvas.draw_image(self._tiles, 
                    [HALF_TILE_SIZE + val * TILE_SIZE, HALF_TILE_SIZE], 
                    [TILE_SIZE, TILE_SIZE], 
                    [col * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE, 
                     row * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE], 
                    [TILE_SIZE, TILE_SIZE])
                    
    def start(self):
        """
        Start the game.
        """        
        self._game.reset()
        self._game.new_tile()
        self._game.new_tile()

def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()
