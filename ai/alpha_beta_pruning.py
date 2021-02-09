import subprocess
import time

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

  st = time.time()
  out = proc.communicate(data.encode("utf-8"))
  total = time.time() - st
  print(total)

  piece, x, y = out[0].decode('utf-8').split(" ")
  piece = mm[int(piece)]
  x = int(x)
  y = int(y)

  print(piece , x, y)

  return {
    'color': "black",
    'piece' : piece,
    'new_position' : [y, x]
  }


def alpha_beta_pruning_native(board, color, depth, isUserWhite):
  if depth == 0:
    return evaluate_board(board, isUserWhite)

  st = time.time()
  moves_list = helper.get_moves(board, color, filter_piece=None, isUserWhite=isUserWhite)

  if len(moves_list) == 0:
    return None

  best_move = moves_list[0]
  best_score = float('-inf')

  alpha = float('-inf')
  beta = float('inf')

  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    score = alpha_beta(clone_board, OPPOSITE[color], alpha, beta, depth - 1, isUserWhite, True)
    if score > best_score:
      best_move = move
      best_score = score

  total = time.time() - st
  print(total)
  print(best_move, best_score)

  return best_move


def alpha_beta(board, color, alpha, beta, depth, isUserWhite, isMin = False):
  if depth == 0 or helper.game_over(board, color):
    return evaluate_board(board, isUserWhite)

  moves_list = helper.get_moves(board, color, filter_piece=None, isUserWhite=isUserWhite)

  score = float('inf') if isMin else float('-inf')
  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    if not isMin:
      score = max(score, alpha_beta(
        clone_board, OPPOSITE[color], alpha, beta, depth - 1, isUserWhite, True))
      alpha = max(alpha, score)
      if beta <= alpha:
        return score
    else:
      score = min(score, alpha_beta(
        clone_board, OPPOSITE[color], alpha, beta, depth - 1, isUserWhite, False))
      beta = min(beta, score)
      if beta <= alpha:
        return score

  return score
