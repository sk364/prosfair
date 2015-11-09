
import imp

import json

chessboard = json.load(open("../common/initial_state.json"))


rules = imp.load_source('chess_basic_rules','../common/rules.py')


opposite_army = { "white" : "black" , "black" : "white" }

def generate_board(board,move):
	board[move['color']][move['piece']] = move['new_position']
	return board

#print chessboard



#print generate_board( chessboard,  { 'color':'white' , 'piece' : 'king' , 'new_position' : [4,4] })
#

#Debugged checkmate
def in_checkmate(board,color):
	
	if in_check(board,color) == True and not rules.legal_king_moves(board,color,"king"):
		return True
		

	if not rules.legal_king_moves(board,color,"king"):		#if moves of the king are null, then it is surrounded by its own pieces and is safe.
		return False

	for x in rules.legal_king_moves(board,color,"king"):
		 if in_check(generate_board(board,{"color":color,"new_pos":x,"piece":"king"}),color) == False:
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
		





def evaluate_goodness(board,color,depth):


	if depth == 0 : return 0.0

	if in_checkmate(board,color) or in_check(board,color):	return -1.0
	if in_checkmate(board,opposite_army[color]) or in_check(board,opposite_army[color]): return 1.0

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
			moves_list = moves_list + [ [ color,x,move, -evaluate_goodness( generate_board(board,{ 'color':color, 'piece':x, 'new_position':move}),opposite_army[color],depth-1)]]
	
	
	return moves_list




print evaluate_goodness(chessboard,"white",1)


	
