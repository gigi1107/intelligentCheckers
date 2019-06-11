


import numpy as np
import sys
from copy import deepcopy
import math 

# DOC--------------------------
# Functions that can be used to test the Board object:
# 1. print_board()
# 2. set_player(player): valid player is 1 or 2
# 3. assign(x,y,value): update the matrix at row =2, col = y to be the value passed in 

# Functions that are helpers to calculating valid moves:
# 1. possible_moves: main function to start calculating valid moves.
#   Requires a board object, returns a list of all possible moves
# 2. piece_valid_move: called by possible_moves 
#   Returns a list of valid moves, given a piece x,y coordinate
# 3. piece_valid_double_jump: called by piece_valid_move
#   Returns a list of possible double jumps after a given jump
# 4. merge_jump: called by possible_moves
# - combine double jumps into 1 action. 
# - BUG: cannot combine 3+ jump
# 5. can_move(action): returns true if action is valid. 
# 
# Functions that are helpers to create evaluation function:
# 1. eval_board: basic evaluation function based on how many pieces are there
# 2. eval_board2: complex evaluation function based on the distance of each piece
# 3. get_red: called by eval_board2. Returns a list of x,y coordinate for 
#   all red pieces. 
# 4. get_black: called by eval_board2. Returns a list of x,y coordinate for 
#   all red pieces. 

# Functions that functionality of the Board:
#  1. constructor
#  2. new_board() populates a 8x8 matrix with red and black pieces
#  3. game_setup()
#  4. action(matrix) - takes in a matrix, and returns the best_move 
#  5. make_move(action)
#  6. check_for_king - scans the board and changes a normal piece to king piece
#   if it reaches the end
#  7. is_terminal() - check if board reaches end state
#   BUG: doesn't check if there's no possible move. only check for 0 pieces 
#  8. move_piece(x1,y1,x2,y2) - move a piece given starting and ending coordinate
#  9. move_piece2(action) - move a piece given an action 
#  10. delete_piece(x,y) - remove a piece, changing it to dash '-'
# 
# Functions for AI engine: 
#   1. main minimax with depth = 3
#   returns the best move (Action)
#   2. minimax - recursive 
#   with alpha beta pruning to improve process time
#   This calls possible_moves 

# TODO: fix hard-coding values

MAX_DEPTH = 3
BOARD_SIZE = 8


class Board:

    # Red is computer
    # Black is user
    # Black always go first 
    def __init__(self):
        self.matrix = self.new_board()
        self.blackCount = 12
        self.redCount = 12
        self.isRedWinner = False
        self.curr_player = 1


    
    def new_board(self):
        #matrix = np.ones((3,3))

        # Using numpy function to print pattern
        # Initilize intial 8x8 matrix with 0s
        
        matrix = np.zeros((8,8),dtype=str)
        #matrix = np.array((8,8), unicode = True)
        matrix[:] = '-'
        # Fill with 1 for alternate rows and columns
        
        #matrix = [[0] * 8 for i in range(8)]
        matrix[1::2,::2] = 'x'
        matrix[::2,1::2] = 'x'
        matrix[3,::1] = '-'
        matrix[4,::1] = '-'

        for y in range(8):
            for x in range(3):
                if matrix[x][y] == 'x':
                    #matrix[x][y]= Piece(RED)
                    matrix[x][y] = 'r'
            for x in range(5, 8):
                if matrix[x][y] == 'x':
                    matrix[x][y]= 'b'
            
        return matrix

    # Returns true if action is valid
    def can_move(self, action):
        allow_moves = self.possible_moves(self)
        if action in allow_moves:
            x = action[0][0]
            y = action[0][1]
            if self.matrix[x][y] == 'r' or self.matrix[x][y] == 'R':
                return True
            else:
                return False
        else:
            return False
    
    # --------------------------
    # This function takes in a coordinate of a piece
    # and returns all the allowable moves that piece can make 
    def piece_valid_move(self, board, x, y, allow_moves_in):
        allow_moves = [(),()]
        #allow_moves.append(allow_moves_in)
        allow_moves = allow_moves_in
        # If player is red
        if (board.curr_player == 1):
            
            # If piece is in the corner
            # Only 1 direction allowable
            
            
            # If piece is not in the right corner
            # then check for all Forward Right moves
            if (y!=7 and x < 7):
                # Normal move: Direction 4
                if (board.matrix[x+1][y+1] == '-'):
                    allow_moves.append(((x,y),(x+1,y+1)))

                # Jump move
            
                if (board.matrix[x+1][y+1] == 'b'  or board.matrix[x+1][y+1] == 'B'): 
                    if (x+1<7 and y+1<7):
                        if ( board.matrix[x+2][y+2] is not None and board.matrix[x+2][y+2] == '-'):
                            allow_moves.append(((x,y),(x+2,y+2)))
                          
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x+2, y+2)
                            
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y+2, allow_moves) 
                
            # If piece is not in the left corner
            # then check all the Forward Left moves 
            if (y!= 0 and x<7):
                # Normal move: Direction 8 
                if (board.matrix[x+1][y-1] == '-'):
                    allow_moves.append(((x,y),(x+1,y-1)))
                # Jump move
                if (board.matrix[x+1][y-1] == 'b' or board.matrix[x+1][y-1] == 'B'): 
                    if (x+1<7 and y-1>0):
                        if (board.matrix[x+2][y-2] == '-'):
                            allow_moves.append(((x,y),(x+2,y-2))) 
                            # Make a copy of board given move
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x+2, y-2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y-2,allow_moves) 

            # -----------------------------------
            # if King, also check for Backward Left and Right
            if board.matrix[x][y] == 'R':
                # Backward Left
                if (y!=0 and x>0):
                    # Normal move: Direction 11
                    if (board.matrix[x-1][y-1] == '-'):
                        allow_moves.append(((x,y),(x-1,y-1)))

                    # Jump move
            
                    if (board.matrix[x-1][y-1] == 'b'  or board.matrix[x-1][y-1] == 'B'):
                        if (x-1>0 and y-1>0): 
                            if (board.matrix[x-2][y-2] == '-'):
                                allow_moves.append(((x,y),(x-2,y-2))) 
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x-2, y-2)
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y-2, allow_moves) 
                
            # If piece is not in the left corner
            # then check all the Backward Left moves 
                if (y!= 7 and x>0):
                    # Normal move: Direction 1 
                    if (board.matrix[x-1][y+1] == '-'):
                        allow_moves.append(((x,y),(x-1,y+1)))
                    # Jump move
                    if (board.matrix[x-1][y+1] == 'b'  or board.matrix[x-1][y+1] == 'B'):
                        if (x-1>0 and y+1<7): 
                            if (board.matrix[x-2][y+2] == '-'):
                                allow_moves.append(((x,y),(x-2,y+2)))
                                # Make a copy of board given move
                                # recursive call to make sure everything
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x-2, y+2)
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y+2,allow_moves) 
        # -----------------------------------------------
        #     
        # If current player is black
        if (board.curr_player == 2):
            # If piece is not in the right corner
            # then check for all Backward Right moves
            if (y!=7 and x>0):
            # Normal move: Direction 1
                if (board.matrix[x-1][y+1] == '-'):
                    allow_moves.append(((x,y),(x-1,y+1)))

                # Jump move
        
                if (board.matrix[x-1][y+1] == 'r'  or board.matrix[x-1][y+1] == 'R'): 
                    if (x-1>0 and y+1<7):
                        if (board.matrix[x-2][y+2] == '-'):
                            allow_moves.append(((x,y),(x-2,y+2)))
                            # Make a copy of board given move
                            # and check if subsequent jumps are possible
                            board_copy = Board()
                            board_copy.clone_board(board)
                            
                            board_copy.move_piece(x, y, x-2, y+2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y+2, allow_moves) 
            
            # If piece is not in the left corner
            # then check all the Backward Left moves 
            if (y!= 0 and x>0):
                # Normal move: Direction 11
                if (board.matrix[x-1][y-1] == '-'):
                    allow_moves.append(((x,y),(x-1,y-1)))
                # Jump move
                if (board.matrix[x-1][y-1] == 'r'  or board.matrix[x-1][y-1] == 'R'): 
                    if (x-1>0 and y-1>0):
                        if (board.matrix[x-2][y-2] == '-'):
                            allow_moves.append(((x,y),(x-2,y-2))) 
                            # Make a copy of board given move
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x-2, y-2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y-2,allow_moves) 

            # -----------------------------------
            # if King, also check for Forward Left and Right
            # Black Kings can move downward the board 
            if board.matrix[x][y] == 'B':
                if (y!=7 and x<7):
                    # Normal move: Direction 4
                    if (board.matrix[x+1][y+1] == '-'):
                        allow_moves.append(((x,y),(x+1,y+1)))

                    # Jump move
            
                    if (board.matrix[x+1][y+1] == 'r' or board.matrix[x+1][y+1] == 'R'): 
                        if (x+1<7 and y+1<7):
                            if (board.matrix[x+2][y+2] == '-'):
                                allow_moves.append(((x,y),(x+2,y+2))) 
                                # Make a copy of board given move
                                # and check if subsequent jumps are possible
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x+2, y+2)
                                allow_moves = board_copy.piece_valid_move(board_copy, x+2,y+2, allow_moves) 
                
                # If piece is not in the left corner
                # then check all the Forward Left moves 
                if (y!= 0 and x<7):
                    # Normal move: Direction 8
                    if (board.matrix[x+1][y-1] == '-'):
                        allow_moves.append(((x,y),(x+1,y-1)))
                    # Jump move
                    if (board.matrix[x+1][y-1] == 'r'  or board.matrix[x+1][y-1] == 'R'): 
                        if (x+1<7 and y-1>0):
                            if (board.matrix[x+2][y-2] == '-'):
                                allow_moves.append(((x,y),(x+2,y-2))) 
                                # Make a copy of board given move
                                # recursive call to make sure everything
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x+2, y-2)
                                allow_moves = board_copy.piece_valid_move(board_copy, x+2,y-2,allow_moves)
        
        return allow_moves 

        
    def clone_matrix(self, matrix):
        for x in range(8):
            for y in range(8):
                self.matrix[x][y] = matrix[x][y]
    def clone_board(self, board):
        for x in range(8):
            for y in range(8):
                self.matrix[x][y] = board.matrix[x][y]
    
    def piece_valid_double_jump(self, board, x,y, allow_moves_in):
        allow_moves = [(),()]
       
        allow_moves = allow_moves_in
        # If player is red
        if (board.curr_player == 1):
            
            if (y!=7 and x < 7):

                # Jump move
            
                if (board.matrix[x+1][y+1] == 'b'  or board.matrix[x+1][y+1] == 'B'): 
                    if (x+1<7 and y+1<7):
                        if (board.matrix[x+2][y+2] == '-'):
                            allow_moves.append(((x,y),(x+2,y+2)))
                            # Make a copy of board given move
                            # and check if subsequent jumps are possible
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x+2, y+2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y+2, allow_moves) 
                
            # If piece is not in the left corner
            # then check all the Forward Left moves 
            if (y!= 0 and x<7):
      
                # Jump move
                if (board.matrix[x+1][y-1] == 'b' or board.matrix[x+1][y-1] == 'B'): 
                    if (x+1<7 and y-1>0):
                        if (board.matrix[x+2][y-2] == '-'):
                            allow_moves.append(((x,y),(x+2,y-2))) 
                            # Make a copy of board given move
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x+2, y-2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y-2,allow_moves) 

            # -----------------------------------
            # if King, also check for Backward Left and Right
            if board.matrix[x][y] == 'R':
                # Backward Left
                if (y!=0 and x>0):

                    # Jump move
            
                    if (board.matrix[x-1][y-1] == 'b'  or board.matrix[x-1][y-1] == 'B'): 
                        if (x-1>0 and y-1>0):
                            if (board.matrix[x-2][y-2] == '-'):
                                allow_moves.append(((x,y),(x-2,y-2))) 
                                # Make a copy of board given move
                                # and check if subsequent jumps are possible
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x-2, y-2)
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y-2, allow_moves) 
                
            # If piece is not in the left corner
            # then check all the Backward Left moves 
                if (y!= 7 and x>0):
                    # Jump move
                    if (board.matrix[x-1][y+1] == 'b'  or board.matrix[x-1][y+1] == 'B'): 
                        if(x-1>0 and y+1<7):
                            if (board.matrix[x-2][y+2] == '-'):
                                allow_moves.append(((x,y),(x-2,y+2)))
                                # Make a copy of board given move
                                # recursive call to make sure everything
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x-2, y+2)
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y+2,allow_moves) 
            
        # If current player is black
        if (board.curr_player == 2):
            # If piece is not in the right corner
            # then check for all Backward Right moves
            if (y!=7 and x>0):

                # Jump move
        
                if (board.matrix[x-1][y+1] == 'r'  or board.matrix[x-1][y+1] == 'R'): 
                    if (x-1>0 and y+1<7):
                        if (board.matrix[x-2][y+2] == '-'):
                            allow_moves.append(((x,y),(x-2,y+2)))
                            # Make a copy of board given move
                            # and check if subsequent jumps are possible
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x-2, y+2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y+2, allow_moves) 
            
            # If piece is not in the left corner
            # then check all the Backward Left moves 
            if (y!= 0 and x>0):

                # Jump move
                if (board.matrix[x-1][y-1] == 'r'  or board.matrix[x-1][y-1] == 'R'): 
                    if (x-1>0 and y-1>0):
                        if (board.matrix[x-2][y-2] == '-'):
                            allow_moves.append(((x,y),(x-2,y-2))) 
                            # Make a copy of board given move
                            board_copy = Board()
                            board_copy.clone_board(board)
                            board_copy.move_piece(x, y, x-2, y-2)
                            allow_moves = board_copy.piece_valid_double_jump(board_copy, x-2,y-2,allow_moves) 

            # -----------------------------------
            # if King, also check for Forward Left and Right
            # Black Kings can move downward the board 
            if board.matrix[x][y] == 'B':
                if (y!=7 and x<7):

                    # Jump move
            
                    if (board.matrix[x+1][y+1] == 'r' or board.matrix[x+1][y+1] == 'R'): 
                        if (x+1<7 and y+1<7):
                            if (board.matrix[x+2][y+2] == '-'):
                                allow_moves.append(((x,y),(x+2,y+2))) 
                                # Make a copy of board given move
                                # and check if subsequent jumps are possible
                                board_copy = Board()
                                board_copy.clone_board(board)
                    
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y+2, allow_moves) 
                
                # If piece is not in the left corner
                # then check all the Forward Left moves 
                if (y!= 0):
                    # Jump move
                    if (board.matrix[x+1][y-1] == 'r'  or board.matrix[x+1][y-1] == 'R'): 
                        if (x+1<7 and y-1>0):
                            if (board.matrix[x+2][y-2] == '-'):
                                allow_moves.append(((x,y),(x+2,y-2))) 
                                # Make a copy of board given move
                                # recursive call to make sure everything
                                board_copy = Board()
                                board_copy.clone_board(board)
                                board_copy.move_piece(x, y, x+2, y-2)
                                allow_moves = board_copy.piece_valid_double_jump(board_copy, x+2,y-2,allow_moves)
        
        return allow_moves 

        
    # Takes a board as an input
    # Call necessary functions to get all possible moves 
    # Returns a list of all possible move given a board state
    def possible_moves(self, board):
        allow_moves = []

        # If current is red, check for only r moves
        if board.curr_player == 1:
            for x in range(8):
                for y in range(8):
                    if (board.matrix[x][y] == 'r' or board.matrix[x][y] == 'R'):
                        allow_moves = board.piece_valid_move(board,x,y, allow_moves)
        
        # If current is black, check for only b moves
        if board.curr_player == 2:
            for x in range(8):
                for y in range(8):
                    if (board.matrix[x][y] == 'b' or board.matrix[x][y] == 'B'):
                        allow_moves = board.piece_valid_move(board,x,y, allow_moves)
        allow_merged = board.merge_jump(allow_moves)

        return allow_merged

    def game_setup(self):
        
        self.print_board()
        self.action(self.matrix)

        
    # Main function used by front-end
    # Takes in a 2d array 
    # Returns the best move
    # Also call the move function

    def action(self, front_end_matrix):
        temp = Board()
        temp.clone_matrix(front_end_matrix)
        move = temp.main_minimax(temp.matrix)
        print("Move gotten in ACTION: ", move)
        
        # DEBUGGING
        print("Print matrix")
        print(temp.matrix)
        print("Current possible moves")
        templist = temp.possible_moves(temp)
        print(templist)


        #    self.make_move(move)
        if move is not None:
            temp = Board()
            temp.matrix = front_end_matrix
            

        else: 
            print("Empty move")
        return move
    
    # Perform the move of the piece
    # check for King 

    # def make_move(self, move, temp):

    #     temp.move_piece2(move)
    #     # Scanning the matrix to see if the total amount of black
    #     # and red has changed:
    #     red_count = 0
    #     black_count = 0
    #     for x in range(8):
    #         for y in range(8):
    #             if self.matrix[x][y] == 'r' or self.matrix[x][y] == 'R':
    #                 red_count +=1
    #             if self.matrix[x][y] == 'b' or self.matrix[x][y] == 'B':
    #                 black_count +=1
                
    #     if self.redCount > red_count:
    #         print("Jump happened! red - 1")
    #         self.redCount = red_count

    #     if self.blackCount > black_count:
    #         print("Jump happened! black - 1")
    #         self.blackCount = black_count

    #     print("red count: ", self.redCount)
    #     print("black count: ", self.blackCount)
        
    #     temp.check_for_king()

    #     print("Board after move: ")
    #     temp.print_board()


    # This function checks if a piece reaches the end
    # and turn it into a king          
    def check_for_king(self):
        for y in range(8):
            if self.matrix[7][y] == 'r':
                self.matrix[7][y] = 'R'
                print("New king for Red at ", '7',y)

        for y in range(8):
            if self.matrix[0][y] == 'b':
                self.matrix[0][y] = 'B'
                print("New king for Black at ", '0',y)

    # Main minimax function
    # Start the minimax process
    # Calls minimax() and get a tuple
    # Returns the best_move action
    def main_minimax(self, matrix):
        temp = Board()
        temp.matrix = matrix
        best_move = temp.minimax(MAX_DEPTH,self,-math.inf, math.inf, True, None)


        if best_move is None:
            print("BEST MOVE IS NONE")
            moves = temp.possible_moves(temp)
            return moves[0]
        return best_move[1]

    def minimax(self, depth, board, alpha, beta, maxPlayer, best_move):
        if depth == 0 or board.is_terminal(board) == True:
            return board.eval_board2(),best_move
        if maxPlayer: 
            # Initialize to negative infinity
            maxEval = -math.inf
            #board.curr_player = 1
            moves = board.possible_moves(board)
            for action in moves: 
                #print(action)
                board_copy = Board()
                board_copy.clone_board(board)
                board_copy.move_piece2(action)
                eval_score = board.minimax(depth-1,board_copy,alpha,beta, False,best_move)
                if (eval_score[0] > maxEval):
                    maxEval = eval_score[0]
                    best_move = action
                alpha= max(alpha, eval_score[0])
                if beta <= alpha:
                    break
            return maxEval,best_move
        else: #if min player
            minEval = math.inf
            # RESET CURR PLAYER???? 
            #board.curr_player = 2
            moves = board.possible_moves(board) 
            for action in moves:
                board_copy = Board()
                board_copy.clone_board(board)
                board_copy.move_piece2(action)
                eval_score = board.minimax(depth-1,board_copy, alpha,beta, True, best_move)
                
                if (eval_score[0] < minEval):
                    minEval = eval_score[0]
                    best_move = action
                beta = min(beta,eval_score[0])
                
                if beta<= alpha:
                    break
            return minEval,best_move

    # Returns a simple evaluation depending who the current player is
    # by counting the amount of pieces left on the board
    # This can be used to determine the total game score
    def eval_board(self, board):
        red, black = 0,0 
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y]== 'r': red +=1
                elif board.matrix[x][y] == 'b': black +=1

                # And if it's a king piece 
                elif board.matrix[x][y] == 'R': red+=1.5
                elif board.matrix[x][y] == 'B': black+= 1.5 

 
                if board.curr_player == 1: 
                    return red-black
                else:
                    return black-red
    # This function takes no parameter
    # and returns a list of the coordinate of all red pieces 
    # on the current board
    def get_red(self):
        red_pieces = []
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y] == 'r' or self.matrix[x][y]=='R':
                    piece_location = (x,y)
                    red_pieces.append(piece_location)
        return red_pieces

    # This function takes no parameter
    # and returns a list of the coordinate of all black pieces 
    # on the current board
    def get_black(self):
        black_pieces =[]
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y] == 'b' or self.matrix[x][y] == 'B':
                    piece_location = (x,y)
                    black_pieces.append(piece_location)
        return black_pieces

    # This is an improved evaluation function 
    # using mathematical equation 
    # It uses one of the basic checkers strategy: keeping pieces together
    # This evaluation function achieves this by calculating the distance
    # between the pieces on the board 
    # and chooses the state with the lesser distance 

    # The distance equation is taken from the internt
    # Reference is below
    def eval_board2(self):
        # If ending state
        if self.is_terminal(self):
            if self.redCount < self.blackCount:
                return -math.inf
            else:
                return math.inf


        # Start tracking the evaluation
        score = 0
        pieces = 0
        if self.curr_player == 1:
            pieces = self.get_red()  
            score_temp = -1
        if self.curr_player == 2:
            pieces = self.get_black()
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
    
    # Checks whether it's a terminal state 
    # This only accounts for all  
    def is_terminal(self, board):
        black_left = False
        red_left = False
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y] == 'r' or board.matrix[x][y] == 'R': red_left = True
                if board.matrix[x][y] == 'b' or board.matrix[x][y] == 'B': black_left = True
                if black_left and red_left:
                    return False
        return True
    


    # Remove a piece from its current position 
    # Takes row,col
    # Returns nothing
    def delete_piece(self, x, y):
        self.matrix[x][y] = '-'
    
    # This function moves a piece given the action tuple ((x,y), (a,b))
    def move_piece2(self, action):
        x1 = action[0][0]
        y1 = action[0][1]
        x2 = action[1][0]
        y2 = action[1][1]
        
        # Moving the piece
        self.matrix[x2][y2] = self.matrix[x1][y1]
        # Call delete piece at the old [row][col]
        self.delete_piece(x1,y1)

    # This functions move a piece given coordinates
    def move_piece(self, x1,x2,y1,y2):
        # Moving the piece
        self.matrix[x2][y2] = self.matrix[x1][y1]
        # Call delete piece at the old [row][col]
        self.delete_piece(x1,y1)

    # This function is used for testing purposes 
    # It assigns matrix[x][y] the value given 
    def assign(self, x, y, value):
        if self.matrix[x][y] is not None:
            self.matrix[x][y] = value
    # This function prints the 2D array 
    def print_board(self):
        print(self.matrix)
    
    
    # This function allows users to set the current player 
    # between 1 (red) and 2(black)
    def set_player(self, player):
        if (player == 1 or player == 2):
            self.curr_player = player
    

    # This is a helper function for possible_moves
    # It merges double jumps 
    # BUG: It cannot merge triple jumps due to indexing issue. 
    def merge_jump(self, movelist):
        newmove = [list(item) for item in movelist]
        to_be_pop =[]
        for x in range(len(movelist)-1):
            begin = newmove[x][1]
            end = newmove[x+1][0]
            if begin == end:
                newmove[x][1] = newmove[x+1][1]
                to_be_pop.append(x+1)
        for x in range(len(to_be_pop)-1):
            newmove.pop(x)
        return newmove

# This function merges double jumps into 1 action 
### BUG: doesn't work for more than 2 jumps because indexing issue          

def interface(board):
    game = Board()
    
    move = game.action(board)
    return move
