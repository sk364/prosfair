import imp
import json

chessboard = json.load(open("../common/initial_state.json"))
rules = imp.load_source('chess_basic_rules','../common/rules.py')


opposite_army = { "white" : "black" , "black" : "white" }

def generate_board(board,move):
	board[move['color']][move['piece']] = move['new_position']
	return board


#Debugged checkmate
def in_checkmate(board,color):
	
	if in_check(board,color) == True and not rules.legal_king_moves(board,color,"king"):
		return True
		

	if not rules.legal_king_moves(board,color,"king"):		#if moves of the king are null, then it is surrounded by its own pieces and is safe.
		return False

	for x in rules.legal_king_moves(board,color,"king"):
		 if in_check(generate_board(board,{"color":color,"new_position":x,"piece":"king"}),color) == False:
			return False

	return True



def in_check(board,color):
	oc = opposite_army[color]
	moves = []
	for x in board[oc].keys():
		if   "king"   in x:
			moves = moves +  rules.legal_king_moves(board,oc,x)
		elif "queen"  in x:
			moves = moves +  rules.legal_queen_moves(board,oc,x)
		elif "bishop" in x:
			moves = moves +  rules.legal_bishop_moves(board,oc,x)
		elif "knight" in x: 
			moves = moves +  rules.legal_knight_moves(board,oc,x)
		elif "rook"   in x:
			moves = moves +  rules.legal_rook_moves(board,oc,x)
		elif "pawn"   in x:
			moves = moves +  rules.legal_pawn_moves(board,oc,x)

	if board[color]['king'] in moves:
		return True

	return False
		

def game_over(board,color):
	if in_checkmate(board,color) or in_checkmate(board,opposite_army[color]) :	return True
	return False

def evaluate_board(board,color):
	if in_checkmate(board,color) or in_check(board,color):	return -1.0
	if in_checkmate(board,opposite_army[color]) or in_check(board,opposite_army[color]): return 1.0
 	##TODO: here only two extremes cases has only been handled
	##      need to write the middle cases, which will include
	## 	the current position of the player's pieces. 
	return 0.0 



def get_moves(board,color):
	moves_list  = []
	moves = []

	for x in board[color].keys():
		if   "king"   in x:
			moves = rules.legal_king_moves(board,color,x)
		elif "queen"  in x:
			moves = rules.legal_queen_moves(board,color,x)
		elif "bishop" in x:
			moves = rules.legal_bishop_moves(board,color,x)
		elif "knight" in x:
			moves = rules.legal_knight_moves(board,color,x)
		elif "rook"   in x:
			moves = rules.legal_rook_moves(board,color,x)
		elif "pawn"   in x:
			moves = rules.legal_pawn_moves(board,color,x)
		
		for move in moves:
			moves_list = moves_list + [ {"color": color,"piece":x,"new_position":move}  ]
	
	return moves_list

def minimax(board,color,depth):


	if depth == 0 : return evaluate_board(board,color)
	
	moves_list = get_moves(board,color)

	assert len(moves_list) > 0

	best_move = moves_list[0]
	best_score = float('-inf')

	for move in moves_list:
		clone_board = generate_board(board,move)
		score = min_play(clone_board,opposite_army[color],depth)
		if score > best_score:
			best_move= move
			best_score = score
	
	return best_move
	

def min_play(board,color,depth):
	if game_over(board,color) or depth <= 0:
		return evaluate_board(board,color)

	moves_list = get_moves(board,color)
	best_score = float('inf')
	
	for move in moves_list:
		clone_board = generate_board(board,move)
		score  =max_play(clone_board,opposite_army[color],depth-1)
		print "evaluating move : ", move, score
		if score < best_score:
			best_move = move
			best_score = score

	return best_score



def max_play(board,color,depth):
	if game_over(board,color) or depth <= 0 :
		return evaluate_board(board,color)

	moves_list = get_moves(board,color)

	best_score = float('-inf')

	for move in moves_list:
		clone_board = generate_board(board,move)
		score = min_play(clone_board,color,depth-1)
		print "evaluating move : ", move,score

		if score > best_score:
			best_move = move
			best_score = score
	
	return best_score




print minimax(chessboard,"white",1)
