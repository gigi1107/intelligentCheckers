from flask import Flask
from flask import render_template, url_for, request, redirect
import os
from checkers.forms import SubmitForm
import ast

def update_board(board, move):
	print(move)
	prev_square_raw = move.split(" ")[0]
	next_square_raw = move.split(" ")[1]

	next_square = int(next_square_raw.split("-")[2])
	print(next_square)
	row = next_square%8
	column = next_square // 8
	

	board[column][row] = 'b'

	prev_square = int(prev_square_raw.split("-")[2])
	prev_row = prev_square % 8
	prev_col = prev_square // 8

	board[prev_col][prev_row] = ''

	row_diff = abs(row - prev_row)
	col_diff = abs(column - prev_col)

	if row_diff == 2 and col_diff == 2:
		print("TAKE THAT PIECE")
		#calculate sqaure between and make it blank
		if column > prev_col:
			middle_col = prev_col + 1
			middle_row = prev_row - 1
		else:
			middle_col = prev_col + 1
			middle_row = prev_row + 1
		print("middle row and col")
		print(middle_row)
		print(middle_col)
		board[middle_col][middle_row] = ''


	board[0][0] = ''
	board[2][4] = 'r'

	##GET COMPUTER MOVE HERE AND UPDATE BOARD THAT WAY TOO
	return board

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

		print("HIIIII")
		move = request.args.get('move')
		board = request.args.getlist('board')
	

		clean_board = []
		for element in board:

			new_element = ast.literal_eval(element)
			clean_board.append(new_element)

		print(move)
		
		clean_board = update_board(clean_board, move)
		

		
		return redirect(url_for('showBoard', board = clean_board))
			

	

	@app.route('/board',methods=['GET', 'POST'])

	def showBoard():

		board = request.args.getlist('board')
		clean_board = []
		for element in board:

			new_element = ast.literal_eval(element)
			clean_board.append(new_element)


		print(clean_board)

		form = SubmitForm()
	

		if request.method == 'GET':
			return render_template('checkerboard.html', form=form,  board= clean_board, move=None)
		elif not form.validate():
			return render_template('checkerboard.html', form=form,  board=clean_board, move = None)
		else:
			return redirect(url_for('getPlayerMove', move=form.keywords.data, board = clean_board))


	@app.route('/')

	def startGame():
		board  = []
		for i in range(8):
			inner = []
			for j in range(8):
				if(j == 0 or j == 1):
					inner.append("r");
				elif( j == 6 or j == 7):
					inner.append("b");
				else:
					inner.append(" ");
			board.append(inner)
		
		return redirect(url_for('showBoard' , board  = board))



		

	return app