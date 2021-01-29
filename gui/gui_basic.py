import copy
import json
import re 
import sys

import pygame

from pygame.locals import *
from common.constants import (
  OPPOSITE,
  DEPTH,
  SIZE,
  GRAY,
  WHITE,
  BLUE,
  IMAGE_DIR
)
from common import rules
from common import helper_functions as helper
from ai import alpha_beta_pruning

chessboard1 = json.load(open("./common/initial_state.json"))
chessboard2 = json.load(open("./common/initial_state.json"))
chessboard3 = json.load(open("./common/initial_state.json"))

#created 3 chessboards for now
chessboards = [chessboard1, chessboard2, chessboard3]
chessboard = chessboards[0]   #current board set to the first.

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))

def get_chess_square(x, y):
  return [ x // (SIZE // 8) + 1, y // (SIZE // 8) + 1 ]

def get_chess_square_reverse(a, b):
  return ((a - 1) * SIZE // 8, (b - 1) * SIZE // 8)  

def get_chess_square_border(r, s):
  return ((r - 1) * SIZE // 8 + 2, (s - 1) * SIZE // 8 + 2)
  
def draw_chessboard(board, moves = None):
  screen.fill(WHITE)

  # draw chess blocks
  startX = 0
  startY = 0
  for idx in range(0, 8):
    startX = 0 if idx % 2 == 0 else SIZE // 8
    for __ in range(0, 8):
      pygame.draw.rect(screen, GRAY, ((startX, startY), (SIZE // 8, SIZE // 8)))
      startX += 2 * SIZE // 8
    startY += SIZE // 8 

  # place the correspoding images of the pieces on the blocks
  for army in board.keys():
    for piece in board[army].keys():
      img = pygame.image.load(IMAGE_DIR + army + "_" + re.findall('[a-z]+', piece)[0] + '.png')
      screen.blit(
        img, (
          board[army][piece][1] * SIZE // 8 - SIZE // 8 + SIZE // 80,
          board[army][piece][0] * SIZE // 8 - SIZE // 8 + SIZE // 80
        )
      )

  # if any piece is selected and has some legal moves then display blue squares on corresponding valid move block
  if moves is not None:
    for move in moves:
      pygame.draw.rect(screen, BLUE, (get_chess_square_reverse(move[1], move[0]), (SIZE // 8, SIZE // 8)))

      color = WHITE if (move[1] + move[0]) % 2 != 0 else GRAY
      pygame.draw.rect(screen, color, (get_chess_square_border(move[1], move[0]), (SIZE // 8 - 4, SIZE // 8 - 4)))

      for army in board.keys():
        for piece in board[army].keys():
          if board[army][piece][1] == move[1] and board[army][piece][0] == move[0]:
            img = pygame.image.load(IMAGE_DIR + army + "_" + re.findall('[a-z]+', piece)[0] + '.png')
            screen.blit(
              img, (
                board[army][piece][1] * SIZE // 8 - SIZE // 8 + SIZE // 80,
                board[army][piece][0] * SIZE // 8 - SIZE // 8 + SIZE // 80
              )
            )

  pygame.display.update()


def play_cpu_move(board, color, current_board_idx):
  global chessboards
  cpu_move = alpha_beta_pruning.alpha_beta_pruning_native(board, OPPOSITE[color], DEPTH)

  chessboards[current_board_idx] = helper.generate_board(board, cpu_move)
  board = chessboards[current_board_idx]

  draw_chessboard(board)
  return board


def play_move(board, color, old_pos, current_board_idx):
  old_x, old_y = old_pos
  x, y = pygame.mouse.get_pos()
  new_x, new_y = get_chess_square(x, y)

  valid = False
  for army in board.keys():
    for piece in board[army].keys():
      if board[army][piece][1] == old_x and board[army][piece][0] == old_y:
        if "bishop" in piece:
          if [new_y, new_x] in rules.legal_bishop_moves(board, army, piece):
            valid = True
        elif "pawn" in piece:
          if [new_y, new_x] in rules.legal_pawn_moves(board, army, piece):
            valid = True
        elif "knight" in piece:
          if [new_y, new_x] in rules.legal_knight_moves(board, army, piece):
            valid = True
        elif "rook" in piece:
          if [new_y, new_x] in rules.legal_rook_moves(board, army, piece):
            valid = True
        elif "queen" in piece:
          if [new_y, new_x] in rules.legal_queen_moves(board, army, piece):
            valid = True
        elif "king" in piece:
          if [new_y, new_x] in rules.legal_king_moves(board, army, piece):
            valid = True

      #if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
      if valid and army == color:
        board[army][piece][1] = new_x
        board[army][piece][0] = new_y
        killed_piece = None
        for piece, pos in board[OPPOSITE[army]].items():
          if pos[0] == new_y and pos[1] == new_x:
            killed_piece = piece
          if killed_piece and killed_piece in board[OPPOSITE[army]].keys():
            del board[OPPOSITE[army]][killed_piece]
            break

        draw_chessboard(board)

        print("Calculating...")
        return play_cpu_move(board, color, current_board_idx)
  return board


def looping_cpu_vs_human(board):
  draw_chessboard(board)

  cur = 0
  old_x = 0
  old_y = 0
  new_x = 0
  new_y = 0
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
          cur = (cur + 1) % 3
          board = chessboards[cur]

        if event.key == pygame.K_LEFT:
          cur = (cur + 2) % 3
          board = chessboards[cur]

        #updating the screen with the next or prev chessboard
        draw_chessboard(board)
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        old_x, old_y = get_chess_square(x, y)
        moves = []

        for army in board.keys():
          for piece in board[army].keys():
            if board[army][piece][1] == old_x and board[army][piece][0] == old_y:
              moves = [move['new_position'] for move in helper.get_moves(board, color, piece)]

          draw_chessboard(board, moves)
      if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        new_x, new_y = get_chess_square(x, y)

        if new_x != old_x or new_y != old_y:
          board = play_move(board, color, (old_x, old_y), cur)

def looping_cpu_vs_cpu(board):
  global chessboards

  draw_chessboard(board)

  color = "white"
  cur = 0

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
          cur = (cur+1)%3
          board = chessboards[cur]

        if event.key == pygame.K_LEFT:
          cur = (cur+2) % 3
          board = chessboards[cur]

        draw_chessboard(board)

    move = alpha_beta_pruning.alpha_beta_pruning_native(board, color, DEPTH)

    chessboards[cur] = helper.generate_board(board, move)
    board = chessboards[cur]

    color = OPPOSITE[color]

    draw_chessboard(board)

# def looping_human_vs_human(board):
#   global chessboards

#   draw_chessboard(board)

#   cur = 0
#   old_x = 0
#   old_y = 0
#   new_x = 0
#   new_y = 0

#   color = "white"
#   flag = 0

#   while True:
#     for event in pygame.event.get():
#       if event.type == QUIT:
#         pygame.quit()
#         sys.exit()
#         pygame.display.update()
#       if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_RIGHT:
#           cur = (cur + 1) % 3
#           board = chessboards[cur]
#         if event.key == pygame.K_LEFT:
#           cur = (cur + 2) % 3
#           board = chessboards[cur]
#         draw_chessboard(board)
#       if event.type == pygame.MOUSEBUTTONDOWN:
#         if flag == 1:
#           x,y= pygame.mouse.get_pos()
#           new_x,new_y = get_chess_square(x,y//8)
#           #print new_x,new_y
#           valid = False
#           for x in [color]:
#             for k in board[x].keys():
#               if board[x][k][1] == old_x and board[x][k][0] == old_y:
#                 if "bishop" in k:
#                   if [new_y,new_x] in rules.legal_bishop_moves(board,x,k): valid = True
#                 elif "pawn" in k:
#                   if [new_y,new_x] in rules.legal_pawn_moves(board,x,k):   valid = True
#                 elif "knight" in k:
#                   if [new_y,new_x] in rules.legal_knight_moves(board,x,k): valid = True
#                 elif "rook" in k:
#                   if [new_y,new_x] in rules.legal_rook_moves(board,x,k):   valid = True
#                 elif "queen" in k:
#                   if [new_y,new_x] in rules.legal_queen_moves(board,x,k):  valid = True 
#                 elif "king" in k:
#                   if [new_y,new_x] in rules.legal_king_moves(board,x,k): valid = True

#                 # if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
#                 if valid and x == color:
#                   board[x][k][1] = new_x
#                   board[x][k][0] = new_y
#                   killed_piece = None
#                   for k,v in board[OPPOSITE[x]].items():
#                           if v[0] == new_y and v[1] == new_x:
#                                   killed_piece = k

#                   if killed_piece and (killed_piece in board[OPPOSITE[x]].keys()): del board[OPPOSITE[x]][killed_piece]




#                   draw_chessboard(board)
#                   color = OPPOSITE[color] 
#                 break
#           flag = 0
#         else:
#           x,y= pygame.mouse.get_pos()
#           old_x,old_y = get_chess_square(x,y//8)
#           p= []
#           for x in [color]:
#             for k in board[x].keys():
#               if board[x][k][1] == old_x and board[x][k][0] == old_y:
#                 #print k
#                 if "bishop" in k:
#                   p = rules.legal_bishop_moves(board,x,k)
#                 elif "pawn" in k:
#                   p = rules.legal_pawn_moves(board,x,k)
#                 elif "knight" in k:
#                   p = rules.legal_knight_moves(board,x,k)
#                 elif "rook" in k:
#                   p = rules.legal_rook_moves(board,x,k)
#                 elif "queen" in k:
#                   p = rules.legal_queen_moves(board,x,k)
#                 elif "king" in k:
#                   p = rules.legal_king_moves( board,x,k)

#           draw_chessboard(board,p)
#       if event.type == pygame.MOUSEBUTTONUP:
#         x,y= pygame.mouse.get_pos()
#         new_x,new_y = get_chess_square(x,y//8)
                                 
#         if new_x == old_x and new_y == old_y:
#           flag = 1
#           continue
          
#         else:
#           valid = False
#           for x in [color]:
#             for k in board[x].keys():
#               if board[x][k][1] == old_x and board[x][k][0] == old_y:
#                 if "bishop" in k:
#                   if [new_y,new_x] in rules.legal_bishop_moves(board,x,k): valid = True
#                 elif "pawn" in k:
#                   if [new_y,new_x] in rules.legal_pawn_moves(board,x,k):   valid = True
#                 elif "knight" in k:
#                   if [new_y,new_x] in rules.legal_knight_moves(board,x,k): valid = True
#                 elif "rook" in k:
#                   if [new_y,new_x] in rules.legal_rook_moves(board,x,k):   valid = True
#                 elif "queen" in k:
#                   if [new_y,new_x] in rules.legal_queen_moves(board,x,k):  valid = True
#                 elif "king" in k:
#                   if [new_y,new_x] in rules.legal_king_moves(board,x,k): valid = True

#                 #if piece is moved to valid position then update the piece's coordinates and check if it is killing other piece
#                 if valid and x == color:
#                   board[x][k][1] = new_x
#                   board[x][k][0] = new_y
#                   killed_piece = None
#                   for k,v in board[OPPOSITE[x]].items():
#                     if v[0] == new_y and v[1] == new_x:
#                       killed_piece = k

#                   if killed_piece and (killed_piece in board[OPPOSITE[x]].keys()):
#                     del board[OPPOSITE[x]][killed_piece]

#                   draw_chessboard(board)
#                   color = OPPOSITE[color]
#                   break
