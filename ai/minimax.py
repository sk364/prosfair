from ai.cpu import evaluate_board
from common.constants import OPPOSITE
from common import helper_functions as helper

def minimax(board, color, depth):
  if depth == 0:
    return evaluate_board(board, color)

  moves_list = helper.get_moves(board, color)

  if len(moves_list) == 0:
    return None

  best_move = moves_list[0]
  best_score = float('-inf')

  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    score = min_play(clone_board, OPPOSITE[color], depth)
    if score > best_score:
      best_move = move
      best_score = score

  return best_move


def min_play(board, color, depth):
  if helper.game_over(board, color) or depth <= 0:
    return evaluate_board(board, color)

  moves_list = helper.get_moves(board, color)
  best_score = float('inf')

  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    score = max_play(clone_board, OPPOSITE[color], depth-1)
    if score < best_score:
      best_score = score

  return best_score


def max_play(board, color, depth):
  if helper.game_over(board, color) or depth <= 0 :
    return evaluate_board(board, color)

  moves_list = helper.get_moves(board, color)

  best_score = float('-inf')

  for move in moves_list:
    clone_board = helper.generate_board(board, move)
    score = min_play(clone_board, color, depth-1)
    if score > best_score:
      best_score = score

  return best_score
