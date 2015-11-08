import pygame, sys
from pygame.locals import *
import re	
import json
import imp


chessboard = json.load(open("../common/initial_state.json"))
image_dir = "../res/basic_chess_pieces/"
rules = imp.load_source('chess_basic_rules','../common/rules.py')



def get_chess_square(x,y,size):
	SIZE = size/8
	return [ x/size+1,y/size+1]



pygame.init()
screen = pygame.display.set_mode((600, 600))
	

	
def draw_chessboard( chess_board, size):


 
	SIZE = size
 
	 
	GRAY = (150, 150, 150)
	WHITE = (255, 255, 255)

	myfont = pygame.font.SysFont("monospace" , 20)
	 
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
			#screen.blit(label,(startX,startY))
			#screen.blit(label,(startX+100,startY))
			startX += 2* SIZE/8
		startY += SIZE/8 

	for army in chessboard.keys():
		for k in chess_board[army].keys():
			img = pygame.image.load(image_dir + army + "_" + re.findall('[a-z]+',k)[0]+'.png')
			screen.blit(img,( chess_board[army][k][1]*SIZE/8 - SIZE/8, chess_board[army][k][0] * SIZE/8 - SIZE/8 )) 		

	pygame.display.update()
	 

def looping(chess_board,size):
	SIZE = size

	draw_chessboard(chess_board,size)
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
				 #print old_x,old_y
					
			 if event.type == pygame.MOUSEBUTTONUP:
				 x,y= pygame.mouse.get_pos()
				 new_x,new_y = get_chess_square(x,y,SIZE/8)
				 #print new_x,new_y
				 valid = False
				 for x in ['white','black']:
					for k in chess_board[x].keys():
						if chess_board[x][k][1] == old_x and chess_board[x][k][0] == old_y:
							#print k
							if "bishop" in k:
								if [new_y,new_x] in rules.legal_bishop_moves(chess_board,x,k): valid = True
							elif "pawn" in k:
								#print "hey"
								if [new_y,new_x] in rules.legal_pawn_moves(chess_board,x,k):   valid = True
							elif "knight" in k:
								if [new_y,new_x] in rules.legal_knight_moves(chess_board,x,k): valid = True
							elif "rook" in k:
								if [new_y,new_x] in rules.legal_rook_moves(chess_board,x,k):   valid = True
							elif "queen" in k:
								if [new_y,new_x] in rules.legal_queen_moves(chess_board,x,k):  valid = True
							elif "king" in k:
								if [new_y,new_x] in rules.legal_king_moves( chess_board,x,k): valid = True


							if valid:
								chess_board[x][k][1] = new_x
								chess_board[x][k][0] = new_y
				 draw_chessboard(chess_board,size)
				 
			 

			


##main loop ... 
looping( chessboard,600)
