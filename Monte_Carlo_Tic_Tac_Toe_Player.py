"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
	"""
	This function play a game starting with the given player by
	making random moves, alternating between players. 
	It returns when the game is over , by modifing the board
	input
	"""
	# mc_trial pusdo code:
 #    while the game is not won:
 #        get a list of empty squares (there's a board method for that)
 #        randomly choose one of the empty squares
 #        move to the selected square (there's a board method to make a move)
 #        switch the player (call provided.switch_player())
	pass

def mc_update_scores(scores, board, player):
	"""
	This function score the completed board and update the score
	grid
	"""
	pass

def get_best_move(board, scores):
	"""
	This function find all of the empty squares with the maximum 
	score and randomly return one of the as a (row, column) tuple

	scores is a list of lists containing a grid of scores
	"""
	return (0,0)

def mc_move(board, player, trials):
	"""
	This function use the Monte Carlo simulation to described above
	to return a move for the machine player in the form of a
	(row, column) tuple
	"""
 #   mc_move pusdo code:
 #    loop for NTRIALS:
 #        create a clone of the board
 #        pass the clone and the current player to mc_trial()
 #        update the scores using the clone of the board (call mc_update_scores())
 #    find the best move by calling get_best_move()
 #    return the move
 	for i in range(trials):
 		clone_board = board.clone()
 		mc_trial(clone_board, player)
 		scores = 0
 		mc_update_scores(scores, clone_board, player)

 	get_best_move(board, scores)	

	return (0,0)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


# Test suite for individual functions
# import user34_Uc9ea2tRiN_0 as test_ttt
# test_ttt.test_trial(mc_trial)
# print
# test_ttt.test_update_scores(mc_update_scores, MCMATCH, MCOTHER)
# print
# test_ttt.test_best_move(get_best_move)
