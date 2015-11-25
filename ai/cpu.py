import imp
import json
import copy

rules = imp.load_source('chess_basic_rules','common/rules.py')
piece_value = json.load(open("common/chess_piece_priority.json"))
helper = imp.load_source('helper_functions','common/helper_functions.py')

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
	
	#print emperical_eval , risk_eval  , defence_eval 
	
	return risk_eval



	


''' this part of code is related to minimax and not being used due to presence of better alternative over it'''

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









''' this is the better alternative over minimax '''


# this alpha_beta_pruning is called from external c++ program

import subprocess

def alpha_beta_pruning(board,color,depth):

	temp_str = "king queen bishop_1 bishop_2 knight_1 knight_2 rook_1 rook_2 pawn_1 pawn_2 pawn_3 pawn_4 pawn_5 pawn_6 pawn_7 pawn_8".split(" ")
	data= ""

	mm = {}

	for i in xrange(len(temp_str)):
		if temp_str[i] in board['white'].keys(): 
			xy=board['white'][temp_str[i]]
		else:
			xy=[-1,-1]
		
		data = data + str(xy[0]) +" "+ str(xy[1]) + "\n"
		#print xy[0],xy[1]
		mm[i] = temp_str[i]

	for i in xrange(len(temp_str)):
		if temp_str[i] in board['black'].keys():
			xy=board['black'][temp_str[i]]
		else:
			xy=[-1,-1]

		data = data + str(xy[0]) + " " + str(xy[1]) + "\n"
		#print xy[0],xy[1]
		mm[16+i] = temp_str[i]

	#print "\n\n"
	#print data

	if color == "white":
		player=0
	else:
		player=16

	#print "player :"+str(player),"depth : "+str(depth)
	proc = subprocess.Popen(["ai/minimax", str(player), str(depth) ],stdout=subprocess.PIPE,stdin=subprocess.PIPE)

	out = proc.communicate(data)

	#print out
	piece, x, y = out[0].split(" ")
	piece=mm[int(piece)]
	x = int(x) +1
	y = int(y) +1

	print piece , x, y

	return { 'color':"black", 'piece' : piece , 'new_position' : [y,x] }  
	


def alpha_beta_pruning_python_native(board,color,depth):
	if depth == 0 : return evaluate_board(board,color)
        
        moves_list = helper.get_moves(board,color)

        if len(moves_list) == 0: return None

        best_move = moves_list[0]
        best_score = float('-inf')

	alpha = float('-inf')
	beta = float('inf')

        for move in moves_list:
                clone_board = helper.generate_board(board,move)
                score = alpha_beta_min(clone_board, opposite[color], alpha, beta, depth)
                if score > best_score:
                        best_move= move
                        best_score = score
        
        return best_move


def alpha_beta_min(board,color,alpha,beta, depth):
        if depth == 0 or helper.game_over(board, color) :
                return evaluate_board(board,color)

        moves_list = helper.get_moves(board,color)

        for move in moves_list:
                clone_board = helper.generate_board(board,move)

                score = alpha_beta_max(clone_board,opposite[color],alpha,beta,depth-1)
                if score <= beta:
                        return alpha
                if score < alpha:
                        beta = score

        return beta

def alpha_beta_max(board,color,alpha,beta, depth):
        if depth == 0 or helper.game_over(board, color) :
                return evaluate_board(board,color)

        moves_list = helper.get_moves(board,color)

        for move in moves_list:
                clone_board = helper.generate_board(board,move)

                score = alpha_beta_min(clone_board,opposite[color],alpha,beta,depth-1)
                if score >= beta:
                        return beta
                if score > alpha:
                        alpha = score

        return alpha

