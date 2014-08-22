"""
Clone of 2048 game.
"""

#import poc_2048_gui        
#import user34_hbhMz0FBOi_1 as merge_test
#merge_test.run_test(merge)

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    # first stage [2,0,2,4]-->[2,2,4,0]
    len_line = len(line)
    for j in range(len_line):
        for i in range(len_line-1):
            if line[i]==0:
                line[i],line[i+1]=line[i+1],line[i]
    #print line
    # second stage -->[4,0,4,0]
    for i in range(len_line-1):
        if line[i]==line[i+1]:
            line[i],line[i+1]=2*line[i],0
    #print line        
    # third stage -->[4,4,0,0]
    # repeat the operation of first stage
    for j in range(len_line):
        for i in range(len_line-1):
            if line[i]==0:
                line[i],line[i+1]=line[i+1],line[i]
    #print line
            
    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        pass
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        pass
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        pass

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return 0
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return 0
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        pass
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return 0
 
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
