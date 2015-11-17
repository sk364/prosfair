
#Original Author : Sachin Kukreja (skad5455[at]gmail[dot]com)
import json

#board = json.load(open("../common/initial_state.json"))

opposite_army = { "white" : "black" , "black" : "white" }

def legal_king_moves(board,color,king='king'):
	if king not in board[color].keys(): return []
	x , y = board[color][king] 

	king_moves = []
	for i in xrange(3):
		for j in xrange(3):
			if  9 > x+i-1 > 0 and 9 > y+j-1 >0:
				if x+i-1 != x or y+j-1 != y:
					king_moves  = king_moves +  [[x+i-1,y+j-1]]	

	return [ x for x in king_moves if x not in board[color].values() ]


def legal_pawn_moves(board,color,pawn):
	if pawn not in board[color].keys(): return []
	x , y = board[color][pawn]
        pawn_moves = []
	if color == "white" :
		if x==2:
			if 9 > y > 0:
				if [x+2,y] not in board[opposite_army[color]].values():
					pawn_moves = pawn_moves + [[x+2,y]]
		if x<8:
			if 9 > y > 0:
				if [x+1,y] not in board[opposite_army[color]].values():
					pawn_moves = pawn_moves+ [[x+1,y]]
			if y>1:
				if [x+1, y-1] in board[opposite_army[color]].values():
                                        pawn_moves = pawn_moves+ [[x+1,y-1]]
			if y<8:
				if [x+1, y+1] in board[opposite_army[color]].values():
                                        pawn_moves = pawn_moves+ [[x+1,y+1]]
			
	else:
		if x==7:
                 	if 9 > y > 0:
            	                if [x-2,y] not in board[opposite_army[color]].values():
      	                                pawn_moves = pawn_moves + [[x-2,y]]
                if x>1:
          	      	if 9 > y > 0:
                                if [x-1,y] not in board[opposite_army[color]].values():
                             		pawn_moves = pawn_moves+ [[x-1,y]]
                     	if y>1:
                      	  	if [x-1, y-1] in board[opposite_army[color]].values():
                              		pawn_moves = pawn_moves+ [[x-1,y-1]]
                      	if y<8:
                               	if [x-1, y+1] in board[opposite_army[color]].values():
                                	pawn_moves = pawn_moves+ [[x-1,y+1]]


	return[x for x in pawn_moves if x not in board[color].values()]



def legal_bishop_moves(board,color,bishop):
	if bishop not in board[color].keys(): return []
	x , y = board[color][bishop]

        bishop_moves = []
 
	for i in xrange(8):
		if x-i-1>0 and y+i+1<9:
			if [x-i-1,y+i+1] in board[color].values(): break
			bishop_moves = bishop_moves + [[x-i-1,y+i+1]]
			if [x-i-1,y+i+1] in board[opposite_army[color]].values(): break

	for i in xrange(8):
		if x-i-1 > 0 and y-i-1 > 0:
			if [x-i-1,y-i-1] in board[color].values(): break
			bishop_moves = bishop_moves + [[x-i-1,y-i-1]]
			if [x-i-1,y-i-1] in board[opposite_army[color]].values(): break

	for i in xrange(8):
		if x+i+1 < 9 and y-i-1 > 0:
			if [x+i+1,y-i-1] in board[color].values(): break
			bishop_moves = bishop_moves + [[x+i+1,y-i-1]]
			if [x+i+1,y-i-1] in board[opposite_army[color]].values(): break

	for i in xrange(8):
        	if x+i+1 < 9 and y+i+1 < 9:
			if [x+i+1,y+i+1] in board[color].values(): break
                        bishop_moves = bishop_moves + [[x+i+1,y+i+1]]
			if [x+i+1,y+i+1] in board[opposite_army[color]].values(): break

	return [x for x in bishop_moves if x not in board[color].values()]


def legal_knight_moves(board, color, knight):
	if knight not in board[color].keys(): return []
	x , y = board[color][knight]

	knight_moves = []

	if x+2 < 9 and y+1 < 9:
		knight_moves = knight_moves + [[x+2,y+1]]

	if x+1 < 9 and y+2 < 9:
		knight_moves = knight_moves + [[x+1,y+2]]

	if x-1 > 0 and y+2 < 9:
		knight_moves = knight_moves + [[x-1,y+2]]
	
	if x-1 > 0 and y-2 > 0:
		knight_moves = knight_moves + [[x-1,y-2]]

	if x+2 < 9 and y-1 > 0:
		knight_moves = knight_moves + [[x+2,y-1]]

	if x+1 < 9 and y-2 > 0:
		knight_moves = knight_moves + [[x+1,y-2]]

	if x-2 > 0 and y-1 > 0:
		knight_moves = knight_moves + [[x-2,y-1]]

	if x-2 > 0 and y+1 < 9:
		knight_moves = knight_moves + [[x-2,y+1]]	

	return [x for x in knight_moves if x not in board[color].values()]




def legal_rook_moves(board,color,rook):
	if rook not in board[color].keys() : return []
	x , y = board[color][rook]

	rook_moves = []

	for i in xrange(8):
                if x+i+1 < 9:
			if [x+i+1,y] in board[color].values(): break
                        rook_moves = rook_moves + [[x+i+1,y]]
			if [x+i+1,y] in board[opposite_army[color]].values(): break

        for i in xrange(8):
                if x-i-1 > 0:
			if [x-i-1,y] in board[color].values(): break
                        rook_moves = rook_moves + [[x-i-1,y]]
			if [x-i-1,y] in board[opposite_army[color]].values(): break

        for i in xrange(8):
                if y+i+1 < 9:
			if [x,y+i+1] in board[color].values(): break
                        rook_moves = rook_moves + [[x,y+i+1]]
			if [x,y+i+1] in board[opposite_army[color]].values(): break

        for i in xrange(8):
                if y-i-1 > 0:
			if [x,y-i-1] in board[color].values(): break
                        rook_moves = rook_moves + [[x,y-i-1]]
			if [x,y-i-1] in board[opposite_army[color]].values(): break
	
	return [x for x in rook_moves if x not in board[color].values()]

def legal_queen_moves(board, color,queen="queen"):
	if queen not in board[color].keys(): []
	x , y = board[color][queen]

	queen_moves = legal_rook_moves(board,color,queen) + legal_bishop_moves(board,color,queen)

	return [x for x in queen_moves if x not in board[color].values()]

