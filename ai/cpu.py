import imp
import json
import copy

rules = imp.load_source('chess_basic_rules','../common/rules.py')
piece_value = json.load(open("../common/chess_piece_priority.json"))


opposite = { "white" : "black" , "black" : "white" }

def generate_board(board,move):
	new_board = copy.deepcopy(board)
	killed_piece = None
	for k,v in new_board[opposite[move['color']]].iteritems(): 
		if move['new_position'] == v :
			killed_piece = k

	if killed_piece and killed_piece in new_board[opposite[move['color']]].keys() : del new_board[opposite[move['color']]][killed_piece]


	new_board[move['color']][move['piece']] = move['new_position']
	return new_board


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
	oc = opposite[color]
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
	if 'king' in board[color].keys():
		if board[color]['king'] in moves:
			return True

	return False
		

def game_over(board,color):
	if in_checkmate(board,color) or in_checkmate(board,opposite[color]) :	return True
	return False

def if_piece_in_check(board, color,piece):
        oc = opposite[color]

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

        if board[color][piece] in moves:
                return True

        return False

def risk_comparision(board,color):
	return sum([ float(piece_value[x]) for x in board[opposite[color]].keys() if if_piece_in_check(board,opposite[color],x) ]) - sum([ float(piece_value[x]) for x in board[color].keys() if if_piece_in_check(board,color,x) ] ) 		

def defence_comparision(board,color):
	return sum([ float(shielding(board,color,x)) for x in board[color].keys() ]) - sum ([ float(shielding(board,opposite[color],x))  for x in board[opposite[color]].keys() ] )



def get_reverse_map(board):

	white = {}
	black = {}

	for k,v in board["white"].iteritems():
		white[(v[0],v[1])]= k

	for k,v in board["black"].iteritems():
		black[(v[0],v[1])]= k

	return { "white":white , "black":black}



def shielding(board,color,piece):
	## Shielding is how many pieces it's protecting from getting attacked, 
	## one way to calculate it is if it's occupying a position which
		
	if piece not in board[color].keys():	return 0.0

	clone_board = copy.deepcopy(board)
	del clone_board[color][piece]

	positions_with    = set([ (x['new_position'][0],x['new_position'][1]) for x in get_moves(board,opposite[color]      ) ])
	positions_without = set([ (x['new_position'][0],x['new_position'][1]) for x in get_moves(clone_board,opposite[color]) ])

	positions_diff = positions_without - positions_with

	rboard = get_reverse_map(board)

	value  = 0.0

	for x in positions_diff:
		if x in rboard[color].keys():
			value= value + piece_value[rboard[color][x]]


	return value
	

	## now if I remove the piece and try to find out what moves are possible.... and then I put the piece back.. and find out what moves are possible... so the differece can show me 
	## what pieces are actually being protected from this piece..
	


def emperical_comparision(board,color):
	return sum([ float(piece_value[x]) for x in board[color].keys() ]) - sum( [ float(piece_value[x]) for x in board[opposite[color]].keys() ])


def evaluate_board(board,color):
	if in_checkmate(board,color) or in_check(board,color):	return float('-inf')
	if in_checkmate(board,opposite[color]) or in_check(board,opposite[color]): return float('inf')
 	##TODO: here only two extremes cases has only been handled
	##      need to write the middle cases, which will include
	## 	the current position of the player's pieces.

	emperical_eval = emperical_comparision(board,color)	
	risk_eval      = risk_comparision(board,color)
	defence_eval   = defence_comparision(board,color)
	
	print emperical_eval , risk_eval  , defence_eval 
	
	return defence_eval



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

	if len(moves_list) == 0: return None

	best_move = moves_list[0]
	best_score = float('-inf')

	for move in moves_list:
		clone_board = generate_board(board,move)
		score = min_play(clone_board,opposite[color],depth)
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
		score  =max_play(clone_board,opposite[color],depth-1)
		#print "evaluating move : ", move, score
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
		#print "evaluating move : ", move,score

		if score > best_score:
			best_move = move
			best_score = score
	
	return best_score





#print get_reverse_map(chessboard)

#print shielding(chessboard,'white','king')
