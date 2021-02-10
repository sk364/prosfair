import copy
import json
import re
import sys

import pygame

from random import random
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

chessboard = json.load(open('common/initial_state.json'))
"""{
  "black": {
    # "bishop_1": [7, 2],
    # "bishop_2": [7, 5],
    "king": [0, 4],
    "knight_1": [5, 7],
    # "knight_2": [7, 6],
    # "pawn_1": [6, 0],
    # "pawn_2": [6, 1],
    # "pawn_3": [6, 2],
    # "pawn_4": [6, 3],
    # "pawn_5": [6, 4],
    # "pawn_6": [6, 5],
    # "pawn_7": [6, 6],
    # "pawn_8": [6, 7],
    # "queen": [7, 3],
    # "rook_1": [7, 0],
    # "rook_2": [7, 7]
  },
  "white": {
    # "bishop_1": [0, 2],
    # "bishop_2": [0, 5],
    "king": [7, 7],
    # "knight_1": [0, 1],
    # "knight_2": [0, 6],
    "pawn_1": [6, 7],
    "pawn_2": [6, 6],
    # "pawn_3": [1, 2],
    # "pawn_4": [1, 3],
    # "pawn_5": [1, 4],
    # "pawn_6": [1, 5],
    # "pawn_7": [1, 6],
    # "pawn_8": [1, 7],
    # "queen": [0, 3],
    # "rook_1": [0, 0],
    "rook_2": [7, 6]
  }
}"""

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))

def get_chess_square(x, y):
  return [ x // (SIZE // 8), y // (SIZE // 8) ]


def get_chess_square_reverse(a, b):
  return (a * SIZE // 8, b * SIZE // 8)  


def get_chess_square_border(r, s):
  return (r * SIZE // 8 + 2, s * SIZE // 8 + 2)


def flip_board(board):
  temp = dict(board["white"])
  board["white"] = dict(board["black"])
  board["black"] = temp

  temp = board["white"]["king"]
  board["white"]["king"] = board["white"]["queen"]
  board["white"]["queen"] = temp

  temp = board["black"]["king"]
  board["black"]["king"] = board["black"]["queen"]
  board["black"]["queen"] = temp

  return dict(board)

  
def draw_chessboard(board, moves = None, isUserWhite = True):
  screen.fill(WHITE)

  # draw chess blocks
  startX = 0
  startY = 0
  for idx in range(0, 8):
    if isUserWhite:
      startX = 0 if idx % 2 != 0 else SIZE // 8
    else:
      startX = SIZE // 8 if idx % 2 != 0 else 0
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
          board[army][piece][1] * SIZE // 8 + SIZE // 80,
          board[army][piece][0] * SIZE // 8 + SIZE // 80
        )
      )

  # if any piece is selected and has some legal moves then display blue squares on corresponding
  # valid move block
  if moves is not None:
    for move in moves:
      pygame.draw.rect(
        screen, BLUE, (get_chess_square_reverse(move[1], move[0]), (SIZE // 8, SIZE // 8)))

      if not isUserWhite:
        color = WHITE if (move[1] + move[0]) % 2 != 0 else GRAY
      else:
        color = GRAY if (move[1] + move[0]) % 2 != 0 else WHITE
      pygame.draw.rect(
        screen, color, (get_chess_square_border(move[1], move[0]), (SIZE // 8 - 4, SIZE // 8 - 4)))

      for army in board.keys():
        for piece in board[army].keys():
          if board[army][piece][1] == move[1] and board[army][piece][0] == move[0]:
            img = pygame.image.load(
              IMAGE_DIR + army + "_" + re.findall('[a-z]+', piece)[0] + '.png')
            screen.blit(
              img, (
                board[army][piece][1] * SIZE // 8 + SIZE // 80,
                board[army][piece][0] * SIZE // 8 + SIZE // 80
              )
            )

  pygame.display.update()


def play_cpu_move(board, color, isUserWhite):
  cpu_move = alpha_beta_pruning.alpha_beta_pruning_native(
    board, OPPOSITE[color], DEPTH, isUserWhite)
  board = helper.generate_board(board, cpu_move)
  draw_chessboard(board, moves=None, isUserWhite=isUserWhite)

  return board, helper.game_over(board, OPPOSITE[color])


def play_move(board, color, old_pos, isUserWhite):
  old_x, old_y = old_pos
  x, y = pygame.mouse.get_pos()
  new_x, new_y = get_chess_square(x, y)

  valid = False
  for army in board.keys():
    for piece in board[army].keys():
      if board[army][piece][1] == old_x and board[army][piece][0] == old_y:
        moves = helper.get_moves(board, army, filter_piece=piece, isUserWhite=isUserWhite)
        if [new_y, new_x] in [move['new_position'] for move in moves]:
          valid = True

      if valid and army == color:
        board[army][piece][1] = new_x
        board[army][piece][0] = new_y

        for piece, pos in board[OPPOSITE[army]].items():
          if pos[0] == new_y and pos[1] == new_x and piece != "king":
            del board[OPPOSITE[army]][piece]
            break

        draw_chessboard(board, moves=None, isUserWhite=isUserWhite)

        is_over = helper.game_over(board, color)
        if not is_over:
          print("Calculating...")
          return play_cpu_move(board, color, isUserWhite)

        return board, is_over
  return board, False


def looping_cpu_vs_human(board):
  old_x = 0
  old_y = 0
  new_x = 0
  new_y = 0
  color = "white" if round(random() * 100) <= 50 else "black"
  isUserWhite = color == "white"

  if not isUserWhite:
    board = flip_board(board)

  draw_chessboard(board, moves=None, isUserWhite=isUserWhite)

  if not isUserWhite:
    board, _ = play_cpu_move(board, color, isUserWhite)

  game_over = False
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()
      if not game_over:
        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = pygame.mouse.get_pos()
          old_x, old_y = get_chess_square(x, y)
          moves = []

          for army in board.keys():
            for piece in board[army].keys():
              if board[army][piece][1] == old_x and board[army][piece][0] == old_y:
                moves = [
                  move['new_position']
                  for move in helper.get_moves(
                    board, color, filter_piece=piece, isUserWhite=isUserWhite)
                ]

            draw_chessboard(board, moves=moves, isUserWhite=isUserWhite)
        if event.type == pygame.MOUSEBUTTONUP:
          x, y = pygame.mouse.get_pos()
          new_x, new_y = get_chess_square(x, y)

          if new_x != old_x or new_y != old_y:
            board, is_over = play_move(board, color, (old_x, old_y), isUserWhite)
            if is_over:
              # TODO: display message
              game_over = True
              break


def looping_cpu_vs_cpu(board):
  draw_chessboard(board)

  color = "white"

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()

    board, is_over = play_cpu_move(board, color)

    if is_over:
      # TODO: display message
      break

    color = OPPOSITE[color]

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
