import pygame, sys
from   pygame.locals import *
import re	
import json
import imp
import copy

#chessboard = json.load(open("./common/initial_state.json"))

chessboard1 = json.load(open("./common/initial_state.json"))
chessboard2 = json.load(open("./common/initial_state.json"))
chessboard3 = json.load(open("./common/initial_state.json"))

#created 3 chessboards for now
chessboards = [chessboard1, chessboard2, chessboard3]
chessboard = chessboards[0]		#current board set to the first.


image_dir = "./res/basic_chess_pieces/"
rules = imp.load_source('chess_basic_rules','./common/rules.py')
cpu = imp.load_source('chess_minimax_ai','./ai/cpu.py')
helper = imp.load_source('helper_functions','./common/helper_functions.py')

opposite = { "white" : "black" , "black" : "white" } 


def get_chess_square(x,y,size):
	return [ x/size+1,y/size+1]

def get_chess_square_reverse(a,b,size):
	return ((a-1)*size/8,(b-1)*size/8)	

def get_chess_square_border(r, s, size):
        return((r-1)*size/8+2, (s-1)*size/8+2)




pygame.init()
screen = pygame.display.set_mode((600, 600))


	
def draw_chessboard( board, size,p_list = None):


 
	SIZE = size
 
	 
	GRAY = (150, 150, 150)
	WHITE = (255, 255, 255)
	BLUE = ( 0 , 0 , 150)

	screen.fill(WHITE)
	
	#filling gray square blocks of size/8 alternatively 
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

	#placing the correspoding images of the pieces on the blocks
	for army in board.keys():
		for k in board[army].keys():

			img = pygame.image.load(image_dir + army + "_" + re.findall('[a-z]+',k)[0]+'.png')

			screen.blit(img,( board[army][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[army][k][0] * SIZE/8 - SIZE/8+SIZE/80 )) 		

	#if any piece is selected and has some legal moves then display blue squares on corresponding valid move block
	if p_list:
		for p in p_list:
			pygame.draw.rect(screen,BLUE,(get_chess_square_reverse(p[1],p[0],SIZE),(SIZE/8,SIZE/8)))

			if (p[1]+p[0])%2!=0:
                                pygame.draw.rect(screen, WHITE, (get_chess_square_border(p[1], p[0], SIZE), (SIZE/8-4, SIZE/8-4)))
			else:
				pygame.draw.rect(screen, GRAY,  (get_chess_square_border(p[1], p[0], SIZE), (SIZE/8-4, SIZE/8-4)))
			x, y = p[1], p[0]
			for x in ['white','black']:
                                        for k in board[x].keys():
                                                if board[x][k][1] == p[1] and board[x][k][0] == p[0]:                                                                 #print k
                                                        if "bishop" in k:
                                                               	img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))

                                                        elif "pawn" in k:
                                                               	img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))
                                                        elif "knight" in k:
                                                                img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))
                                                              
							elif "rook" in k:
                                                                img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))


                                                        elif "queen" in k:
                                                               	img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))

                                                        elif "king" in k:
                                                                img = pygame.image.load(image_dir + x + "_" + re.findall('[a-z]+',k)[0]+'.png')

                						screen.blit(img,( board[x][k][1]*SIZE/8 - SIZE/8+SIZE/80, board[x][k][0] * SIZE/8 - SIZE/8+SIZE/80 ))





	pygame.display.update()
	 

def looping_cpu_vs_human(board,size):
	global chessboards	
	global flag
	SIZE = size
	
	draw_chessboard(board,size)
	cur=0
	old_x=0
	old_y=0
	new_x=0
	new_y=0
	color = "white"
	
	flag= 0

	while True:
		 
		 for event in pygame.event.get():
			 
			 if event.type == QUIT:
			 	 pygame.quit()
			 	 sys.exit()
			 	 pygame.display.update()
			 
			 #checking for keyboard events
			 if event.type == pygame.KEYDOWN:
				 if event.key == pygame.K_RIGHT:
					cur = (cur+1)%3
					board = chessboards[cur]

			 	 if event.key == pygame.K_LEFT:
					cur = (cur+2)%3
					board = chessboards[cur]
				 #updating the screen with the next or prev chessboard
				 draw_chessboard(board,size)
			 			 

			 if event.type == pygame.MOUSEBUTTONDOWN:
		 		if flag == 1:
					flag =0
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

                                                               	#if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
                                                               	if valid and x == color:
                                                                       	board[x][k][1] = new_x
                                                                       	board[x][k][0] = new_y
                                                                       	killed_piece = None
                                                                       	for k,v in board[opposite[x]].iteritems():
                                                                               	if v[0] == new_y and v[1] == new_x:
                                                                                       	killed_piece = k
                                                                        	if killed_piece and (killed_piece in board[opposite[x]].keys()): 
											del board[opposite[x]][killed_piece]
											break

                                                                                                  
                                                                        draw_chessboard(board,size)
                                                                       	#move = cpu.minimax(board,opposite[x],1) ##depth is 1

									#CPU turn
                                                                       	move = cpu.alpha_beta_pruning(board,opposite[x],3)
                                                                       	#board = helper.generate_board(board,move)

                                                                       	#referencing the new board generated by helper first to chessboard array element
                                                                       	chessboards[cur] = helper.generate_board(board,move)
                                                                       	board = chessboards[cur]

                                                                       	draw_chessboard(board,size)
									 
									break #Break here is necessary since we are deleting a key from the map on which we are iterating
				else:
					print "here"
					x,y= pygame.mouse.get_pos()
			 		old_x,old_y = get_chess_square(x,y,SIZE/8)
		 			p= []
 					for x in ['white','black']:
                                 		for k in board[x].keys():
                                              		if board[x][k][1] == old_x and board[x][k][0] == old_y:                                                        		#print k
                                                       		if "bishop" in k:
                                                               		p= rules.legal_bishop_moves(board,x,k)
                                                       		elif "pawn" in k:
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
				print "here1"
				x,y= pygame.mouse.get_pos()
			 	new_x,new_y = get_chess_square(x,y,SIZE/8)
				
				if new_x == old_x and new_y == old_y:
					flag = 1
					continue
			
				else:	
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
									#if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
								if valid and x == color:
									board[x][k][1] = new_x
									board[x][k][0] = new_y
									killed_piece = None
									for k,v in board[opposite[x]].iteritems():
										if v[0] == new_y and v[1] == new_x:
											killed_piece = k
							
										if killed_piece and (killed_piece in board[opposite[x]].keys()): 
											del board[opposite[x]][killed_piece]
											break
						
													
														
									draw_chessboard(board,size)										#move = cpu.minimax(board,opposite[x],1) ##depth is 1
										#CPU turn
									
									move = cpu.alpha_beta_pruning(board,opposite[x],7)
										#board = helper.generate_board(board,move)
										#referencing the new board generated by helper first to chessboard array element
									chessboards[cur] = helper.generate_board(board,move)
									board = chessboards[cur]

									draw_chessboard(board,size)
									break #Break here is necessary since we are deleting a key from the map on which we are iterating
							 
				 

				 

def looping_cpu_vs_cpu(board,size):
	global chessboards
	draw_chessboard(board,size)
	color = "white"
	cur = 0
	#print board
	while True:
		for event in pygame.event.get():
                         if event.type == QUIT:
                                 pygame.quit()
                                 sys.exit()
                                 pygame.display.update()

			 #checking for keyboard events
			 if event.type == pygame.KEYDOWN:
                                 if event.key == pygame.K_RIGHT:
                                        cur = (cur+1)%3
                                        board = chessboards[cur]

                                 if event.key == pygame.K_LEFT:
                                        cur = (cur+2)%3
                                        board = chessboards[cur]
                                 #updating the screen with the next or prev chessboard
                                 draw_chessboard(board,size)


		move = cpu.alpha_beta_pruning_python_native(board,color,1) #depth is 1
		#move = cpu.alpha_beta_pruning(board,color,7)

		chessboards[cur] = helper.generate_board(board,move)
		board = chessboards[cur]

		color = opposite[color]

		draw_chessboard(board,size)

def looping_human_vs_human(board, size):
	global chessboards
	global flag

        SIZE = size

        draw_chessboard(board,size)
        cur=0
        old_x=0
        old_y=0
        new_x=0
        new_y=0

	color = "white"
	flag = 0

        while True:

                 for event in pygame.event.get():

                         if event.type == QUIT:
                                 pygame.quit()
                                 sys.exit()
                                 pygame.display.update()

                         #checking for keyboard events
                         if event.type == pygame.KEYDOWN:
                                 if event.key == pygame.K_RIGHT:
                                        cur = (cur+1)%3
                                        board = chessboards[cur]

			 	 if event.key == pygame.K_LEFT:
                                        cur = (cur+2)%3
                                        board = chessboards[cur]
                         	 #updating the screen with the next or prev chessboard
                         	 draw_chessboard(board,size)

                         if event.type == pygame.MOUSEBUTTONDOWN:

				if flag == 1:
                                	x,y= pygame.mouse.get_pos()
        	                        new_x,new_y = get_chess_square(x,y,SIZE/8)
					#print new_x,new_y
					valid = False
                                        for x in [color]:
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

                                                                #if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
                                                                if valid and x == color:
                                                                        board[x][k][1] = new_x
                                                                        board[x][k][0] = new_y
                                                                        killed_piece = None
                                                                        for k,v in board[opposite[x]].iteritems():
                                                                                if v[0] == new_y and v[1] == new_x:
                                                                                        killed_piece = k

                                                                        if killed_piece and (killed_piece in board[opposite[x]].keys()): del board[opposite[x]][killed_piece]




                                                                        draw_chessboard(board,size)
									color = opposite[color]	
			                                        break
					flag = 0



				else:
				 	x,y= pygame.mouse.get_pos()
                                	old_x,old_y = get_chess_square(x,y,SIZE/8)
                                 	p= []
                                 	for x in [color]:
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
                                 
				 if new_x == old_x and new_y == old_y:
	
					flag = 1
					continue
				
				 else:
					#print new_x,new_y
                                 	valid = False
                                 	for x in [color]:
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

                                                        	#if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
                                                        	if valid and x == color:
                                                                	board[x][k][1] = new_x
                                                                	board[x][k][0] = new_y
                                                                	killed_piece = None
                                                                	for k,v in board[opposite[x]].iteritems():
                                                                        	if v[0] == new_y and v[1] == new_x:
                                                                                	killed_piece = k

                                                                	if killed_piece and (killed_piece in board[opposite[x]].keys()): del board[opposite[x]][killed_piece]




                                                                	draw_chessboard(board,size)
									color = opposite[color]
									break


##main loop ... 
#looping_cpu_vs_human( chessboard,600)
#looping_cpu_vs_cpu( chessboard,600)
