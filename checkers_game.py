import numpy as np
import sys
import copy
import math 
import pdb

HUMAN = 1
COMPUTER = 2
MAX_DEPTH = 3
BOARD_SIZE = 8

ROW = 0
COL = 1

class Checkerpiece_Move:
    def __init__(self, start_square, end_square):
        self.eval_score = 0
        self.start_square = start_square
        self.end_square = end_square

    def set_eval_score(self, eval_score):
        self.eval_score = eval_score

    def set_start_square(self, start_square):
        self.start_square = start_square

    def set_end_square(self, end_square):
        self.end_square = end_square


class Game_Setting:
    def __init__(self, player, color_computer_pieces, color_human_pieces, blank_space):
        self.player = player
        self.color_computer_pieces = color_computer_pieces
        self.color_human_pieces = color_human_pieces
        self.blank_space = blank_space

    def set_color_computer_pieces(self, color):
        self.color_human_pieces = color

    def set_color_human_pieces(self, color):
        self.color_computer_pieces = color

def get_computer_move(front_end_board):
    board = copy.deepcopy(front_end_board)
    game = Game_Setting(COMPUTER, 'r', 'b','-')
    move = minimax(MAX_DEPTH, board, -math.inf, math.inf, game, None)

    if move is None:
        print("MOVE WAS NONE")
        moves = get_possible_moves(front_end_board, game)
        return moves[0]

    return move[1]

def minimax(depth, board, alpha, beta, game_setting, best_move):
	
    if depth == 0 or is_terminal(board, game_setting):
        return eval_board(board, game_setting), best_move
    maxEval = alpha
    minEval = beta
    possible_moves = get_possible_moves(board, game_setting)
    for move in possible_moves: 
        # print("MOVE: ")
        # print(move.start_square,", ",move.end_square)
        board_copy = copy.deepcopy(board)
        board_after_move = move_piece(move, board_copy, game_setting)
        result = minimax(depth-1, board_after_move, alpha, beta, game_setting, best_move)
        if (game_setting.player == COMPUTER and result[0] > alpha):
            best_move = move
            alpha= max(alpha, result[0])
        elif (game_setting.player == HUMAN and result[0] < minEval):
            minEval = result[0]
            best_move = move
            beta = min(beta, result[0])
        if beta <= alpha:
            break
    return maxEval,best_move

def get_possible_moves(board, game_setting):
	
    allowed_moves = []
    # print("get_possible_moves")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_setting.player == COMPUTER:
               
                if board[row][col].lower() == game_setting.color_computer_pieces:
                    moves = get_valid_moves(board, row ,col, game_setting)
                    
                    if moves:
                        allowed_moves.append(moves)
            else:
                if board[row][col].lower() == game_setting.color_human_pieces:
                    moves = get_valid_moves(board, row, col, game_setting)
                    if moves:
                        allowed_moves.append(moves)
    allowed_moves_merged = merge_moves(allowed_moves)
    return allowed_moves_merged

def merge_moves(moves):

    allowed_moves = []
    # print("merge_moves")
    for move_list in moves:
        for move in move_list:
            allowed_moves.append(move)
    return allowed_moves


# This function takes in a coordinate of a piece
# and returns all the allowable moves that piece can make 
def get_valid_moves(board, x, y, game_setting):
	
    allowed_moves = []
    # print("get_valid_moves")
    diagonal_moves = get_diagonal_moves(board, x, y, game_setting)

    skip_moves = get_skip_moves(board, x, y, [],  game_setting)

    for d in diagonal_moves:
        allowed_moves.append(d)
    for s in skip_moves:
        allowed_moves.append(s)
    return allowed_moves

def get_diagonal_moves(board, row, col, game_setting):
	
    diagonal_moves = []
    # print("get_diagonal_moves")
    if game_setting.player == COMPUTER:
        moves_delta = [(1,1), (1,-1)]
        king_moves_delta = [(-1,-1), (-1, 1)]
    else: 
        moves_delta = [(-1,-1), (-1, 1)]
        king_moves_delta = [(1,1), (-1,1)]
    for move in moves_delta:
        end_row = row + move[ROW]
        end_col = col + move[COL]
        if end_row < BOARD_SIZE  and end_col < BOARD_SIZE and end_row >=0 and end_col >= 0:
            if board[end_row][end_col] == game_setting.blank_space:
                diagonal_moves.append(Checkerpiece_Move((row,col), (end_row,end_col)))
    if is_king(board, row, col, game_setting):
        for king_move in king_moves_delta:
            end_row = row + king_move[ROW]
            end_col = col + king_move[COL]
            if end_row < BOARD_SIZE  and end_col < BOARD_SIZE and end_row >=0 and end_col >= 0:
                if board[end_row][end_col] == game_setting.blank_space:
                    diagonal_moves.append(Checkerpiece_Move((row,col), (end_row, end_col)))

    return diagonal_moves

def is_king(board, row, col, game_setting):
	
    return board[row][col].isupper()

#todo double, triple jumps
def get_skip_moves(board, row, col, moves_in, game_setting):
	
    skip_moves = moves_in
    # print("get_skip_moves")
    if game_setting.player == COMPUTER:
        skip_moves_delta = [(2,-2), (2,2)]
        king_skip_moves_delta = [(-2,-2), (-2, 2)]
    else: 
        skip_moves_delta = [(-2,-2), (-2, 2)]
        king_skip_moves_delta = [(2,-2), (2,2)]
    for skip in skip_moves_delta:
        end_row = row + skip[ROW]
        end_col = col + skip[COL]
        if end_row < BOARD_SIZE  and end_col < BOARD_SIZE and end_row >=0 and end_col >= 0:
            if board[end_row][end_col]  == game_setting.blank_space:
                if board[row + (skip[ROW]//2)][col + (skip[COL]//2)] == game_setting.color_human_pieces:
                    
                    skip_moves.append(Checkerpiece_Move((row,col), (end_row,end_col)))
    if is_king(board, row, col, game_setting):
        for king_skip in king_skip_moves_delta:
            end_row = row + king_skip[ROW]
            end_col = col + king_skip[COL]
            if end_row < BOARD_SIZE  and end_col< BOARD_SIZE and end_row >=0 and end_col >= 0:
                if board[end_row][end_col] == game_setting.blank_space:
                    if board[row + (king_skip[ROW]//2)][col + (king_skip[COL]//2)] == game_setting.color_human_pieces:
                        skip_moves.append(Checkerpiece_Move((row,col), (end_row, end_col)))
    return skip_moves

def get_computer_count(board, game_setting):
	
    computer_pieces = []
    # print("get_computer_count")
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y].upper() == game_setting.color_computer_pieces.upper():
                piece_location = (x,y)
                computer_pieces.append(piece_location)
    return computer_pieces

def get_human_count(board, game_setting):
	
    human_pieces =[]
    # print("get_human_count")
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y].upper() == game_setting.color_human_pieces.upper():
                piece_location = (x,y)
                human_pieces.append(piece_location)
    return human_pieces

# This is an improved evaluation function 
# using mathematical equation 
# It uses one of the basic checkers strategy: keeping pieces together
# This evaluation function achieves this by calculating the distance
# between the pieces on the board 
# and chooses the state with the lesser distance 
def eval_board(board, game_setting):
	
    # If ending state
    # print("eval_board")
    if is_terminal(board, game_setting):
        if len(get_computer_count(board, game_setting)) < len(get_human_count(board, game_setting)):
            return -math.inf
        else:
            return math.inf
    # Start tracking the evaluation
    score = 0
    pieces = 0
    if game_setting.player == COMPUTER:
        pieces = get_computer_count(board, game_setting) 
        score_temp = -1
    if game_setting.player == HUMAN:
        pieces = get_human_count(board, game_setting)
        score_temp =1

    # This defense algorithm is meant to keep 
    # pieces as close to each other as they can be
    # Reference: https://github.com/codeofcarson/Checkers/blob/master/minmax.py
    distance = 0
    for piece1 in pieces:
        for piece2 in pieces:
            if piece1 == piece2:
                continue
        dx = abs(piece1[0] - piece2[0])
        dy = abs(piece1[1] - piece2[1])
        distance += dx**2 + dy**2
    distance /= len(pieces)
    if distance != 0 and score_temp != 0:
        score = 1.0/distance * score_temp
    return score           

def is_terminal(board, game_setting):
    black_left = False
    red_left = False
    # print("is_terminal")
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            
            if board[x][y].upper() == game_setting.color_computer_pieces.upper(): 
                red_left = True
            if board[x][y].upper() == game_setting.color_human_pieces.upper(): 
                black_left = True
            if black_left and red_left:
                return False
    return True

def move_piece(move, board, game_setting):
	
    row_end, col_end = move.end_square
    # print("move_piece")
    row_start, col_start = move.start_square
    board[row_end][col_end] = board[row_start][col_start]
    board[row_start][col_start] = game_setting.blank_space
    return board
