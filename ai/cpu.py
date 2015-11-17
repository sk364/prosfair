import imp
import json
import copy

rules = imp.load_source('chess_basic_rules','../common/rules.py')
piece_value = json.load(open("../common/chess_piece_priority.json"))
helper = imp.load_source('helper_functions','../common/helper_functions.py')

opposite = { "white" : "black" , "black" : "white" }


def emperical_comparision(board,color):
	return sum([ float(piece_value[x]) for x in board[color].keys() ]) - \
		sum( [ float(piece_value[x]) for x in board[opposite[color]].keys() ])

def risk_comparision(board,color):
	return sum([ float(piece_value[x]) for x in board[opposite[color]].keys() if helper.if_piece_under_attack(board,opposite[color],x) ]) - \
		sum([ float(piece_value[x]) for x in board[color].keys() if helper.if_piece_under_attack(board,color,x) ] ) 		

def defence_comparision(board,color):
	return sum([ float(helper.shielding(board,color,x)) for x in board[color].keys() ]) - \
		sum ([ float(helper.shielding(board,opposite[color],x))  for x in board[opposite[color]].keys() ] )



def evaluate_board(board,color):
	if helper.in_checkmate(board,color) or helper.in_check(board,color):	return float('-inf')
	if helper.in_checkmate(board,opposite[color]) or helper.in_check(board,opposite[color]): return float('inf')
 	##TODO: here only two extremes cases has only been handled
	##      need to write the middle cases, which will include
	## 	the current position of the player's pieces.

	emperical_eval = emperical_comparision(board,color)	
	risk_eval      = risk_comparision(board,color)
	defence_eval   = defence_comparision(board,color)
	
	print emperical_eval , risk_eval  , defence_eval 
	
	return risk_eval





def minimax(board,color,depth):

	if depth == 0 : return evaluate_board(board,color)
	
	moves_list = helper.get_moves(board,color)

	if len(moves_list) == 0: return None

	best_move = moves_list[0]
	best_score = float('-inf')

	for move in moves_list:
		clone_board = helper.generate_board(board,move)
		score = min_play(clone_board,opposite[color],depth)
		if score > best_score:
			best_move= move
			best_score = score
	
	return best_move
	

def min_play(board,color,depth):
	if helper.game_over(board,color) or depth <= 0:
		return evaluate_board(board,color)

	moves_list = helper.get_moves(board,color)
	best_score = float('inf')
	
	for move in moves_list:
		clone_board = helper.generate_board(board,move)
		score  =max_play(clone_board,opposite[color],depth-1)
		#print "evaluating move : ", move, score
		if score < best_score:
			best_move = move
			best_score = score

	return best_score



def max_play(board,color,depth):
	if helper.game_over(board,color) or depth <= 0 :
		return evaluate_board(board,color)

	moves_list = helper.get_moves(board,color)

	best_score = float('-inf')

	for move in moves_list:
		clone_board = helper.generate_board(board,move)
		score = min_play(clone_board,color,depth-1)
		#print "evaluating move : ", move,score

		if score > best_score:
			best_move = move
			best_score = score
	
	return best_score

