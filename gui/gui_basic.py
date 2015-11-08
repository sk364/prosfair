import pygame, sys
from pygame.locals import *
import re	
import json



chessboard = json.load(open("../common/initial_state.json"))
image_dir = "../res/basic_chess_pieces/"


def get_chess_square(x,y,size):
	SIZE = size/8
	return [ x/size+1,y/size+1]



pygame.init()
screen = pygame.display.set_mode((600, 600))
	

	
def draw_chessboard( chess_board, size):


 
	SIZE = size
 
	 
	BLACK = (150, 150, 150)
	WHITE = (255, 255, 255)

	myfont = pygame.font.SysFont("monospace" , 20)
	#label = myfont.render("King",1,(150,150,150))
	 
	### MAIN BLOCK ###
	 
	screen.fill(WHITE)
	 
	numRows = 0
	startX = 0
	startY = 0
	 
	for e in range(0, 8):
		if e%2 == 0 :
			startX = 0 
		else:
			startX = SIZE/8
		for e2 in range(0, 8):
			pygame.draw.rect(screen, BLACK, ((startX, startY), (SIZE/8, SIZE/8)))
			#screen.blit(label,(startX,startY))
			#screen.blit(label,(startX+100,startY))
			startX += 2* SIZE/8
		startY += SIZE/8 
	'''
	for army in chessboard.keys():		
		for k in chess_board[army].keys():
			label = myfont.render(k,1,(150,150,150))
			screen.blit(label,( chess_board[army][k][1]*SIZE/8 - SIZE/8,chess_board[army][k][0] * SIZE/8 - SIZE/8))
	'''

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
				 print old_x,old_y
					
			 if event.type == pygame.MOUSEBUTTONUP:
				 x,y= pygame.mouse.get_pos()
				 new_x,new_y = get_chess_square(x,y,SIZE/8)
				 print new_x,new_y
				 for x in ['white','black']:
					for k in chess_board[x].keys():
						if chess_board[x][k][1] == old_x and chess_board[x][k][0] == old_y:
							print k
							chess_board[x][k][1] = new_x
							chess_board[x][k][0] = new_y
				 draw_chessboard(chess_board,size)
				 
			 

			



looping( chessboard,600)
