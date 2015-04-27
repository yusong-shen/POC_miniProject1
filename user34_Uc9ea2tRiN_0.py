"""
Week 2, Principles of Computing
Testing module for Tic-Tac-Toe
Paul 2014/6/24
"""
import poc_simpletest
import poc_ttt_provided as provided


def set_board(board, arrangement):
    """ Convenience function to set entire board """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            board.move(row, col, arrangement[row][col])


def test_trial(mc_trial):
    """ Test for mc_trial() """

    print "Testing the mc_trial function."

    # Create a TestSuite object
    suite = poc_simpletest.TestSuite()

    my_board = provided.TTTBoard(3)
    mc_trial(my_board, provided.PLAYERO)
    suite.run_test(my_board.check_win() is not None, True,
                   "Test 1: mc_trial completes 3x3 game")

    my_board = provided.TTTBoard(4)
    mc_trial(my_board, provided.PLAYERO)
    suite.run_test(my_board.check_win() is not None, True,
                   "Test 2: mc_trial completes 4x4 game")

    suite.report_results()


def manual_scoring(mc_update_scores, mcmatch, mcother,
                   scores, player, arrangement):
    """ Perform one trial of scoring """

    my_board = provided.TTTBoard(3)
    set_board(my_board, arrangement)
    mc_update_scores(scores, my_board, player)

    print my_board
    print "Player =", provided.STRMAP[player], scores


def test_update_scores(mc_update_scores, mcmatch, mcother):
    """ Test for mc_update_scores() """

    print "Testing the mc_update_scores function with a sequence of scoring."
    print "Try setting different MCMATCH/MCOTHER values for this test."
    print "MCMATCH:", mcmatch
    print "MCOTHER:", mcother
    print

    # Create a TestSuite object
    suite = poc_simpletest.TestSuite()
    scores = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    manual_scoring(mc_update_scores, mcmatch, mcother, scores,
                   provided.PLAYERX, [[2, 1, 3], [3, 2, 1], [2, 3, 2]])
    suite.run_test(scores,
                   [[mcmatch, 0.0, -mcother], [-mcother, mcmatch, 0.0],
                    [mcmatch, -mcother, mcmatch]],
                   "Test 1: X won, player is X")

    manual_scoring(mc_update_scores, mcmatch, mcother, scores,
                   provided.PLAYERO, [[2, 1, 3], [3, 2, 1], [2, 3, 2]])
    suite.run_test(scores,
                   [[mcmatch + mcother, 0.0, -mcother - mcmatch],
                    [-mcother - mcmatch, mcmatch + mcother, 0.0],
                    [mcmatch + mcother, -mcother - mcmatch,
                     mcmatch + mcother]],
                   "Test 2: Same game, X won, player is O")

    manual_scoring(mc_update_scores, mcmatch, mcother, scores,
                   provided.PLAYERX, [[2, 3, 2], [3, 3, 2], [3, 2, 3]])
    suite.run_test(scores,
                   [[mcmatch + mcother, 0.0, -mcother - mcmatch],
                    [-mcother - mcmatch, mcmatch + mcother, 0.0],
                    [mcmatch + mcother, -mcother - mcmatch,
                     mcmatch + mcother]],
                   "Test 3: Tied game")

    manual_scoring(mc_update_scores, mcmatch, mcother, scores,
                   provided.PLAYERX, [[1, 3, 2], [2, 3, 1], [1, 3, 2]])
    suite.run_test(scores,
                   [[mcmatch + mcother, mcother, -mcother - 2 * mcmatch],
                    [-mcother - 2 * mcmatch, mcmatch + 2 * mcother, 0.0],
                    [mcmatch + mcother, -mcmatch, mcother]],
                   "Test 4: O won, player is X")

    manual_scoring(mc_update_scores, mcmatch, mcother, scores,
                   provided.PLAYERO, [[1, 2, 2], [3, 3, 3], [3, 2, 2]])
    suite.run_test(scores,
                   [[mcmatch + mcother, 0.0, -2 * mcother - 2 * mcmatch],
                    [-mcother - mcmatch, 2 * mcmatch + 2 * mcother, mcmatch],
                    [2 * mcmatch + mcother, -mcmatch - mcother, 0.0]],
                   "Test 5: O won, player is O")

    suite.report_results()


def test_best_move(get_best_move):
    """ Test for get_best_move() """

    print "Testing the get_best_move function."

    # Create a TestSuite object
    suite = poc_simpletest.TestSuite()

    my_board = provided.TTTBoard(3)
    set_board(my_board, [[2, 3, 2], [1, 1, 1], [1, 2, 3]])
    scores = [[3.0, 5.0, -1.0], [3.0, 2.0, -8.0], [4.0, -2.0, 2.0]]

    print my_board
    print "scores:", scores
    suite.run_test(get_best_move(my_board, scores), (2, 0),
                   "Test 1: Best move")

    my_board = provided.TTTBoard(3)
    set_board(my_board, [[1, 1, 2], [1, 3, 1], [2, 3, 1]])
    scores = [[0.0, 2.0, 1.0], [0.0, 2.0, -1.0], [1.0, -2.0, 2.0]]
    move_set = set([])
    for dummy_idx in range(20):
        move_set.add(get_best_move(my_board, scores))

    print my_board
    print "scores:", scores
    suite.run_test(move_set, set([(0, 1), (2, 2)]),
                   "Test 2: Two possible best moves")

    suite.report_results()