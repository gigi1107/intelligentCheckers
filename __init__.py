from flask import Flask
from flask import render_template, url_for, request, redirect
import os

import ast

def update_board(board, move, original, redscore, blackscore):
	print("update_board")

	print("just inside update board fxn")
	print(redscore)
	print(blackscore)
	next_square = int(move.split("-")[2])

	row = next_square % 8
	column = next_square // 8

	

	prev_square = int(original.split("-")[2])
	prev_row = prev_square % 8
	prev_col = prev_square // 8

	board[prev_row][prev_col] = ''
	board[row][column] = 'b'

	#take pieces jumped
	board= update(board, row, column, prev_row, prev_col)




	return (board, redscore, blackscore)



def update(board, next_row, next_col, prev_row, prev_col):


	row_diff = abs(next_row - prev_row)
	col_diff = abs(next_col - prev_col)

	if row_diff == 1 and col_diff ==1:
		return board
	#base case

	if row_diff == 2 and col_diff ==2:
		#calculate sqaure between and make it blank
		if prev_col > next_col and prev_row > next_row:
			board[prev_row - 1][prev_col - 1]= ''
		elif prev_col < next_col and prev_row > next_row:
			board[prev_row  - 1][prev_row + 1] = ''
		elif prev_col < next_col and prev_row < next_row:
			board[prev_row + 1][prev_col + 1] = ''
		else:
			board[prev_row +1][prev_col - 1] = ''

		return board

	else:
		#recurively calculate jumps
		inter_row = 0
		inter_col = 0
		if next_row < prev_row and next_col > prev_col:
			inter_row = prev_row - 2
			inter_col = prev_col + 2
		elif next_row < prev_row and next_col < prev_col:
			inter_row = prev_row - 2
			inter_col = prev_col - 2
		elif next_row > prev_row and next_col > prev_col:
			inter_row = prev_row + 2
			inter_col = prev_col + 2
		elif next_row > prev_row and next_col < prev_col:
			inter_row = prev_row + 2
			inter_col - prev_col - 2
		elif prev_col == next_col:
			if board[prev_row - 1][prev_col - 1] == 'r':
				inter_row = prev_row - 2
				inter_col = prev_col - 2
			else:
				inter_row = prev_row - 2
				inter_col = prev_col + 2
		#todo add if prev row == next row in case of backwards hops

		board = update(board, inter_row, inter_col, prev_row, prev_col)
		board = update(board, next_row, next_col, inter_row, inter_col)
		print("got here")

		return board



	##GET COMPUTER MOVE HERE AND UPDATE BOARD THAT WAY TOO


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
	    SECRET_KEY='dev',
	)

	if test_config is None:
	    # load the instance config, if it exists, when not testing
	    app.config.from_pyfile('config.py', silent=True)
	else:
	    # load the test config if passed in
	    app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
	    os.makedirs(app.instance_path)
	except OSError:
	    pass


	@app.route('/getplayermove',methods=['GET' , 'POST'])
	def getPlayerMove():
		print("getplayermove")

		
		move = request.args.get('move')
		original_square = request.args.get('original')
		redscore = request.args.get('redscore')
		blackscore = request.args.get('blackscore')
		print("right after retrieval in getPlayerMove")
		print(redscore)
		print(blackscore)


		board = request.args.getlist('board')

		clean_board = []
		for element in board:

			new_element = ast.literal_eval(element)
			clean_board.append(new_element)

	
		
		clean_board, redscore, blackscore= update_board(clean_board, move, original_square, redscore, blackscore)
		
		r_ct = 0
		b_ct = 0
		for row in range(len(clean_board)):
			for col in range(row): 
				if clean_board[row][col] == 'r' or clean_board[row][col] == 'R':
					r_ct += 1
				elif clean_board[row][col] == 'b' or clean_board[row][col] == 'B':
					b_ct += 1

		if r_ct == 0 or b_ct == 0:
			return redirect(url_for('gameOver'))
		


		
		return redirect(url_for('showBoard', board = clean_board, redscore = redscore, blackscore = blackscore))
			

	@app.route('/gameover')

	def gameOver():
		return render_template('gameover.html')

	@app.route('/board',methods=['GET', 'POST'])

	def showBoard():
		print("showboard")

		board = request.args.getlist('board')
		redscore = request.args.get('redscore')
		print("in showboard")
		print("redscore")
		print(redscore)

		blackscore = request.args.get('blackscore')
		print("blackscore")
		print(blackscore)
		clean_board = []
		for element in board:

			new_element = ast.literal_eval(element)
			clean_board.append(new_element)


		if request.method == 'GET':
			return render_template('checkerboard.html', board= clean_board, move=None , redscore=redscore, blackscore=blackscore)
	
		else:
			move = request.form['move_value']
			orig_square = request.form['prev_square']
			return redirect(url_for('getPlayerMove', move=move, original = orig_square, board = clean_board, redscore = redscore, blackscore = blackscore))


	@app.route('/')

	def startGame():
		print("startGame")
		board  = []
		for i in range(8):
			inner = []
			for j in range(8):
				if((i == 0 or i == 2) and j%2 == 0):
					inner.append("r");
				elif (i == 1 and j%2 == 1):
					inner.append("r")
				elif(( i == 5 or i == 7) and j%2 == 1):
					inner.append("b")
				elif (i == 6 and j%2 == 0):
					inner.append("b")
				else:
					inner.append(" ");
			board.append(inner)

		print(board)
		
		redscore = 0
		blackscore = 0
		return redirect(url_for('showBoard' , board  = board, redscore = redscore, blackscore = blackscore))



		

	return app