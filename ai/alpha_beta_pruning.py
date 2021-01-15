import subprocess

from ai.cpu import evaluate_board
from common.constants import OPPOSITE
from common import helper_functions as helper

def alpha_beta_pruning(board, color, depth):
  temp_str = \
    "king queen bishop_1 bishop_2 knight_1 knight_2 rook_1 rook_2 pawn_1 pawn_2 pawn_3 pawn_4 pawn_5 pawn_6 pawn_7 pawn_8".split(" ")

  data= ""
  mm = {}
  for i in range(len(temp_str)):
    for army in board: 
      xy = board[army][temp_str[i]] if temp_str[i] in board[army].keys() else [-1, 1]
      data = data + str(xy[0]) +" "+ str(xy[1]) + "\n"
      mm[i + (16 if army == "black" else 0)] = temp_str[i]

  player = 0 if color == "white" else 16

  proc = subprocess.Popen(["ai/minimax", str(player), str(depth) ],stdout=subprocess.PIPE,stdin=subprocess.PIPE)

  import time
  st = time.time()
  out = proc.communicate(data.encode("utf-8"))
  total = time.time() - st
  print(total)

  piece, x, y = out[0].decode('utf-8').split(" ")
  piece = mm[int(piece)]
  x = int(x) +1
  y = int(y) +1

  print(piece , x, y)

  return {
    'color': "black",
    'piece' : piece,
    'new_position' : [y, x]
  }


def alpha_beta_pruning_native(board,color,depth):
  if depth == 0:
    return evaluate_board(board, color)
      
  moves_list = helper.get_moves(board, color)

  if len(moves_list) == 0:
    return None

  best_move = moves_list[0]
  best_score = float('-inf')

  alpha = float('-inf')
  beta = float('inf')

  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    score = alpha_beta_min(clone_board, OPPOSITE[color], alpha, beta, depth)
    if score > best_score:
      best_move = move
      best_score = score

  print(best_move)

  return best_move


def alpha_beta_min(board, color, alpha, beta, depth):
  if depth == 0 or helper.game_over(board, color) :
      return evaluate_board(board, color)

  moves_list = helper.get_moves(board, color)

  for move in moves_list:
    clone_board = helper.generate_board(board, move)

    score = alpha_beta_max(clone_board, OPPOSITE[color], alpha, beta, depth-1)
    if score <= beta:
      return alpha
    if score < alpha:
      beta = score

  return beta

def alpha_beta_max(board, color, alpha, beta, depth):
  if depth == 0 or helper.game_over(board, color) :
      return evaluate_board(board, color)

  moves_list = helper.get_moves(board, color)

  for move in moves_list:
    clone_board = helper.generate_board(board, move)

    score = alpha_beta_min(clone_board, OPPOSITE[color], alpha, beta, depth-1)
    if score >= beta:
      return beta
    if score > alpha:
      alpha = score

  return alpha
