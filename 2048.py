"""
Clone of 2048 game.

Author : yusong
Date : 11th, August, 2014
"""

import poc_2048_gui       
import random
import user34_hbhMz0FBOi_1 as merge_test
import user34_sw90o8thMp_1 as tile_test
import user34_B88RxBpJcx_0 as poc_2048_testsuite

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
        """
        Call the reset method
        Initialize the grid with nested list whose size is 
        grid_heigh x grid_width
        """

        self.height = grid_height
        self.width = grid_width
        grid = self.reset()
        self.grid = grid
        self.init_dic={UP:[(0,y) for y in range(self.width)],
                       DOWN:[(self.height-1,y) for y in range(self.width)],
                       LEFT:[(x,0) for x in range(self.height)],
                       RIGHT:[(x,self.width-1) for x in range(self.height)]}
        #print self.init_dic
        
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        grid = [[] for i in range(grid_height)]
        for i in range(grid_height):
            grid[i] = [0 for j in range(grid_width)]
        # print grid        
        self.grid = grid        
        return grid

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return "grid_height is %d, grid_width is %d"%(self.height,self.width)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        grid = self.grid
        # the variable used to keep track
        # if the tile has changed
        is_move = False
        # e.g UP:[(0,0),(0,1),(0,2),(0,3)]
        # e.g DOWN:[(4,0),(4,1),(4,2),(4,3)]
        init_tile = self.init_dic[direction]
        #print "init_tile:",init_tile
        # e.g UP:(1,0)
        # e.g DOWN:(-1,0)
        offset = OFFSETS[direction]
        #print "offset:",offset
        # retrieve the row or colum starts with 
        # one of initial tile
        # a little bit tricky
        # consider the up/down and left/right two cases
        # for the up/down 
        if direction<=2: 
            # up/down
            length = self.height
        else:
            # left/right
            length = self.width
        for row,col in init_tile:
            temp =[]
            for i in range(length):
            #get the value of the column/row
            #put the values in a temporary list
                #print "row:",row+offset[0]*i
                #print "col:",col+offset[1]*i
                value = self.get_tile(row+offset[0]*i,col+offset[1]*i)
                #print "value:",value 
                temp.append(value)
            #print "temp %d,%d is  "%(row,col),temp
            # then pass the temp list to the merge(line) function
            move_line = merge(temp)
            # call the set_tile() to set the new value
            for i in range(length):
                self.set_tile(row+offset[0]*i,col+offset[1]*i,move_line[i])
        self.new_tile()  
        
         
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        # random number 1,2...10
        if random.randint(1,10)>9:
            value = 4
        else:
            value = 2
        grid = self.grid
        
        # check how many empty space left, then generate 
        # a random number from 1 to the remaining numbers
        empty_records = []
        for row in range(self.height):
            for col in range(self.width):
                if self.get_tile(row, col) == 0:
                    empty_records.append((row,col))
        # print "empty_pos is %d"%(len(empty_records))            
        if len(empty_records)==0 :
            pass
        else:
            random_num = random.randint(1,len(empty_records))
            # print "random_num is %d"%(random_num)
            # choose a random empty tile,set a new value to it
            c_row = empty_records[random_num-1][0]
            c_col = empty_records[random_num-1][1]
            # print "row:%d, col:%d, value:%d"%(c_row,c_col,value)
            self.set_tile(c_row,c_col,value)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        (self.grid)[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return (self.grid)[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
#merge_test.run_test(merge)
#tile_test.run_test(TwentyFortyEight)
#poc_2048_testsuite.run_test(merge, TwentyFortyEight)