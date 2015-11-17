import pygame, sys
from   pygame.locals import *
import re	
import json
import imp


chessboard = json.load(open("../common/initial_state.json"))
image_dir = "../res/basic_chess_pieces/"
rules = imp.load_source('chess_basic_rules','../common/rules.py')
cpu = imp.load_source('chess_minimax_ai','../ai/cpu.py')
helper = imp.load_source('helper_functions','../common/helper_functions.py')

opposite = { "white" : "black" , "black" : "white" } 


def get_chess_square(x,y,size):
	return [ x/size+1,y/size+1]

def get_chess_square_reverse(a,b,size):
	return ((a-1)*size/8,(b-1)*size/8)	



pygame.init()
screen = pygame.display.set_mode((600, 600))
	

	
def draw_chessboard( board, size,p_list = None):


 
	SIZE = size
 
	 
	GRAY = (150, 150, 150)
	WHITE = (255, 255, 255)
	BLUE = ( 0 , 0 , 150)

	screen.fill(WHITE)
	 
	startX = 0
	startY = 0
	 
	for e in range(0, 8):
		if e%2 == 0 :
			startX = 0 
		else:
			startX = SIZE/8
		for e2 in range(0, 8):
			pygame.draw.rect(screen, GRAY, ((startX, startY), (SIZE/8, SIZE/8)))
			startX += 2* SIZE/8
		startY += SIZE/8 

	for army in board.keys():
		for k in board[army].keys():
			img = pygame.image.load(image_dir + army + "_" + re.findall('[a-z]+',k)[0]+'.png')
			screen.blit(img,( board[army][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[army][k][0] * SIZE/8 - SIZE/8+SIZE/80 )) 		
	if p_list:
		for p in p_list:
			pygame.draw.rect(screen,BLUE,(get_chess_square_reverse(p[1],p[0],SIZE),(SIZE/8,SIZE/8)))

	pygame.display.update()
	 

def looping_cpu_vs_human(board,size):
	SIZE = size

	draw_chessboard(board,size)
	old_x=0
	old_y=0
	new_x=0
	new_y=0

	while True:
			 
		 for event in pygame.event.get():
			 if event.type == QUIT:
				 pygame.quit()
				 sys.exit()
				 pygame.display.update()

			 if event.type == pygame.MOUSEBUTTONDOWN:
				 x,y= pygame.mouse.get_pos()
				 old_x,old_y = get_chess_square(x,y,SIZE/8)
				 p= []
  				 for x in ['white','black']:
                                        for k in board[x].keys():
                                                if board[x][k][1] == old_x and board[x][k][0] == old_y:
                                                        #print k
                                                        if "bishop" in k:
                                                                p= rules.legal_bishop_moves(board,x,k)
                                                        elif "pawn" in k:
                                                                #print "hey"
                                                                p= rules.legal_pawn_moves(board,x,k)
                                                        elif "knight" in k:
                                                                p= rules.legal_knight_moves(board,x,k)
                                                        elif "rook" in k:
                                                                p= rules.legal_rook_moves(board,x,k)
                                                        elif "queen" in k:
                                                                p= rules.legal_queen_moves(board,x,k)
                                                        elif "king" in k:
                                                                p= rules.legal_king_moves( board,x,k)



				 draw_chessboard(board,size,p)
				 #print old_x,old_y
					
			 if event.type == pygame.MOUSEBUTTONUP:
				 x,y= pygame.mouse.get_pos()
				 new_x,new_y = get_chess_square(x,y,SIZE/8)
				 #print new_x,new_y
				 valid = False
				 for x in ['white','black']:
					for k in board[x].keys():
						if board[x][k][1] == old_x and board[x][k][0] == old_y:
							if "bishop" in k:
								if [new_y,new_x] in rules.legal_bishop_moves(board,x,k): valid = True
							elif "pawn" in k:
								if [new_y,new_x] in rules.legal_pawn_moves(board,x,k):   valid = True
							elif "knight" in k:
								if [new_y,new_x] in rules.legal_knight_moves(board,x,k): valid = True
							elif "rook" in k:
								if [new_y,new_x] in rules.legal_rook_moves(board,x,k):   valid = True
							elif "queen" in k:
								if [new_y,new_x] in rules.legal_queen_moves(board,x,k):  valid = True
							elif "king" in k:
								if [new_y,new_x] in rules.legal_king_moves(board,x,k): valid = True


							if valid and x == "white":
								print board
								board[x][k][1] = new_x
								board[x][k][0] = new_y
								killed_piece = None
								for k,v in board[opposite[x]].iteritems():
									if v[0] == new_y and v[1] == new_x:
										killed_piece = k
								
								if killed_piece and (killed_piece in board[opposite[x]].keys()): del board[opposite[x]][killed_piece]
						
													
														
								draw_chessboard(board,size)
								#move = cpu.minimax(board,opposite[x],1) ##depth is 1 
								move = cpu.alphaBetaPruning(board,opposite[x],1)
								board = helper.generate_board(board,move)
								draw_chessboard(board,size)
								break #Break here is necessary since we are deleting a key from the map on which we are iterating
							 
				 

				 

def looping_cpu_vs_cpu(board,size):
	draw_chessboard(board,size)
	color = "white"
	print board
	while True:
		for event in pygame.event.get():
                         if event.type == QUIT:
                                 pygame.quit()
                                 sys.exit()
                                 pygame.display.update()

		move = cpu.minimax(board,color,1)#depth is 1
		board = helper.generate_board(board,move)
		color = opposite[color]
		draw_chessboard(board,size)

def looping_human_vs_human(board, size):
	print "\n\nSorry! This mode is under construction. The game will be updated soon.\n\n"			
		
		
			


##main loop ... 
#looping_cpu_vs_human( chessboard,600)
#looping_cpu_vs_cpu( chessboard,600)
