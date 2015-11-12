
#Evaluating offence values of each piece on the board

import imp

import json

board = json.load(open("../common/initial_state.json"))


rules = imp.load_source('chess_basic_rules','../common/rules.py')


opposite_army = { "white" : "black" , "black" : "white" }

points = { "king":10, "queen": 9, "rook":5, "knight":3, "bishop":3, "pawn":1}

def generate_board(board,move):
        board[move['color']][move['piece']] = move['new_position']
        return board


def if_piece_in_check(board, color,piece):
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

        if board[color][piece] in moves:
                return True

	return False


def evaluate_queen_offence(board,color,queen="queen"):
	
	oc = opposite_army[color]
	
	mx = 0
	pieces = []

	for move in rules.legal_queen_moves(board,color,queen):
		for x in board[oc].keys():
			if if_piece_in_check(generate_board(board,{"color":color,"new_pos":move,"piece":queen}),oc,x):
				pieces = pieces + x
				if points[x] > mx:
					mx = x; 

	return mx

#print evaluate_queen_offence(board,"white","queen")

def evaluate_rook_offence(board,color,rook):

        oc = opposite_army[color]

        mx = 0
        pieces = []

        for move in rules.legal_rook_moves(board,color,bishop):
                for x in board[oc].keys():
                        if if_piece_in_check(generate_board(board,{"color":color,"new_pos":move,"piece":rook}),oc,x):
                                pieces = pieces + x
                                if points[x] > mx:
                                        mx = x;

        return mx

def evaluate_bishop_offence(board,color,bishop):

        oc = opposite_army[color]

        mx = 0
        pieces = []

        for move in rules.legal_bishop_moves(board,color,bishop):
                for x in board[oc].keys():
                        if if_piece_in_check(generate_board(board,{"color":color,"new_pos":move,"piece":bishop}),oc,x):
                                pieces = pieces + x
                                if points[x] > mx:
                                        mx = x;

        return mx

def evaluate_knight_offence(board,color,knight):

        oc = opposite_army[color]

        mx = 0
        pieces = []

        for move in rules.legal_knight_moves(board,color,knight):
                for x in board[oc].keys():
                        if if_piece_in_check(generate_board(board,{"color":color,"new_pos":move,"piece":knight}),oc,x):
                                pieces = pieces + x
                                if points[x] > mx:
                                        mx = x;

        return mx

def evaluate_king_offence(board,color,king="king"):

        oc = opposite_army[color]

        mx = 0
        pieces = []

        for move in rules.legal_king_moves(board,color,king):
                for x in board[oc].keys():
                        if if_piece_in_check(generate_board(board,{"color":color,"new_pos":move,"piece":king}),oc,x):
                                pieces = pieces + x
                                if points[x] > mx:
                                        mx = x;

        return mx

