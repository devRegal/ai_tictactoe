"""
Tic Tac Toe Player
Group : Wesley Zoroya, Geovanny Casian
"""
from collections import Counter
import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    non_empty = 0

    for row in board:
        for cell in row:
            if cell != EMPTY:
                non_empty += 1

    if non_empty % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_cells = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                empty_cells.append((i, j))

    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # creates deep copy of board so that input board will remain intact
    board_copy = copy.deepcopy(board)

    if player(board) == X:
        board_copy[action[0]][action[1]] = X
    else:
        board_copy[action[0]][action[1]] = O
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for symbol in [X, O]:
        # Check rows and columns
        for i in range(3):
            if board[i][0] == symbol and board[i][1] == symbol and board[i][2] == symbol:
                return symbol
            if board[0][i] == symbol and board[1][i] == symbol and board[2][i] == symbol:
                return symbol
        # Check diagonals
        if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
            return symbol
        if board[2][0] == symbol and board[1][1] == symbol and board[0][2] == symbol:
            return symbol

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or all([cell is not EMPTY for row in board for cell in row]):
        return True
    else:
        return False


def score(board):
    """
    Returns the score of the board.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board using alpha-beta pruning.
    """
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        max_value = float('-inf')
        optimal_action = None
        alpha = float('-inf')
        for action in actions(board):
            result_board = result(board, action)
            value = minimax_pruning(result_board, alpha, float('inf'), False)
            if value > max_value:
                max_value = value
                optimal_action = action
            alpha = max(alpha, max_value)
    else:
        min_value = float('inf')
        optimal_action = None
        beta = float('inf')
        for action in actions(board):
            result_board = result(board, action)
            value = minimax_pruning(result_board, float('-inf'), beta, True)
            if value < min_value:
                min_value = value
                optimal_action = action
            beta = min(beta, min_value)

    return optimal_action


def minimax_pruning(board, alpha, beta, is_max):
    """
    Returns the max or min value for the current player on the board using alpha-beta pruning.
    """
    if terminal(board):
        return score(board)

    if is_max:
        # setting the value alpha to change
        v = float('-inf')
        for action in actions(board):
            result_board = result(board, action)
            # recursively call itself, but change alpha <-> beta
            v = max(v, minimax_pruning(result_board, alpha, beta, False))
            alpha = max(alpha, v)
            # check for alpha  >= beta
            if alpha >= beta:
                break
        return v

    else:
        # setting the value beta to change
        v = float('inf')
        for action in actions(board):
            result_board = result(board, action)
            # recursively call itself, but change alpha <-> beta
            v = min(v, minimax_pruning(result_board, alpha, beta, True))
            # check for alpha  >= beta
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v
