import math
import random
import numpy as np
import Vision

ROWS = 6
COLUMNS = 7

HUMAN = 0
AI = 1

EMPTY_PIECE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def is_valid_column(board, col):
    return board[ROWS - 1][col] == 0
    pass


def next_valid_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r
    pass

def make_move(board, row, col, piece_content):
    board[row][col] = piece_content
    pass

def winning_move(board, piece_content):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece_content and board[r][c + 1] == piece_content and board[r][c + 2] == piece_content and board[r][ c + 3] == piece_content:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece_content and board[r + 1][c] == piece_content and board[r + 2][c] == piece_content and board[r + 3][c] == piece_content:
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece_content and board[r + 1][c + 1] == piece_content and board[r + 2][c + 2] == piece_content and board[r + 3][c + 3] == piece_content:
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece_content and board[r - 1][c + 1] == piece_content and board[r - 2][c + 2] == piece_content and board[r - 3][c + 3] == piece_content:
                return True
    return False

def evaluate_block(block, piece_content):
    score = 0
    opp_piece_content = PLAYER_PIECE
    if piece_content == PLAYER_PIECE:
        opp_piece_content = AI_PIECE

    if block.count(piece_content) == 4:
        score += 100
    elif block.count(piece_content) == 3 and block.count(EMPTY_PIECE) == 1:
        score += 5
    elif block.count(piece_content) == 2 and block.count(EMPTY_PIECE) == 2:
        score += 2

    if block.count(opp_piece_content) == 3 and block.count(EMPTY_PIECE) == 1:
        score -= 4

    return score


def score_mechanism(board, piece_content):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(piece_content)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            block = row_array[c:c + 4]
            score += evaluate_block(block, piece_content)

    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            block = col_array[r:r + 4]
            score += evaluate_block(block, piece_content)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            block = [board[r + i][c + i] for i in range(4)]
            score += evaluate_block(block, piece_content)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            block = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_block(block, piece_content)

    return score


def array_valid_columns(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_column(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(array_valid_columns(board)) == 0

def alpha_beta_connect4(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = array_valid_columns(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_mechanism(board, AI_PIECE))
    if maximizingPlayer:
        best_score = -math.inf
        best_column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_valid_row(board, col)
            temp_board = board.copy()
            make_move(temp_board, row, col, AI_PIECE)
            new_score = alpha_beta_connect4(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > best_score:
                best_score = new_score
                best_column = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_column, best_score

    else:  # Minimizing player
        best_score = math.inf
        best_column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_valid_row(board, col)
            temp_board = board.copy()
            make_move(temp_board, row, col, PLAYER_PIECE)
            new_score = alpha_beta_connect4(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < best_score:
                best_score = new_score
                best_column = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_column, best_score


def print_board(board):
    print(np.flip(board, 0))


board = create_board()
game_over = False
Player_turn = HUMAN

while not game_over:

    if Player_turn == HUMAN:
            board = Vision.BoardUpdate(board)  # this where we use vision
            if winning_move(board, PLAYER_PIECE):
                game_over = True
            Player_turn += 1
            Player_turn = Player_turn % 2

    # AI PLAYER
    elif Player_turn == AI:
        col, score = alpha_beta_connect4(board, 5, -math.inf, math.inf, True)

        if is_valid_column(board, col):
            row = next_valid_row(board, col)
            make_move(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                game_over = True
            Player_turn += 1
            Player_turn = Player_turn % 2