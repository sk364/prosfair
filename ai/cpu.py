import json
import subprocess

from common import helper_functions as helper
from common.constants import OPPOSITE, PIECE_VALUE
from common.piece_square_tables import PIECE_SQUARE_MAP


# def risk_comparision(board, color):
#   return sum(
#     [ float(PIECE_VALUE[piece]) for piece in board[OPPOSITE[color]].keys()
#       if helper.if_piece_under_attack(board, OPPOSITE[color], piece) ]
#   ) - sum(
#     [ float(PIECE_VALUE[piece]) for piece in board[color].keys() if helper.if_piece_under_attack(board, color, piece) ]
#   )


# def defence_comparision(board, color):
#   return sum(
#     [ float(helper.shielding(board, color, piece)) for piece in board[color].keys() ]
#   ) - sum (
#     [ float(helper.shielding(board, OPPOSITE[color], piece)) for piece in board[OPPOSITE[color]].keys() ]
#   )

def compute_piece_value(board, color, is_opposition = False):
  sum_of_pieces = 0
  for piece in board[color].keys():
    y, x = board[color][piece]
    piece_value = PIECE_VALUE[piece]
    piece_name = piece.split('_')[0]
    piece_sq_values = PIECE_SQUARE_MAP[piece_name]
    if not is_opposition:
      piece_square_value = piece_sq_values[y][x]
    else:
      piece_square_value = piece_sq_values[7 - y][7 - x]

    sum_of_pieces += (float(piece_value) + float(piece_square_value))
  return sum_of_pieces


def evaluate_board(board, color):
  """
  evaluates the board using
   - piece values
   - piece square tables
  """
  if helper.in_checkmate(board, color):
    return float('-inf')
  if helper.in_checkmate(board, OPPOSITE[color]):
    return float('inf')

  sum_of_pieces_1 = compute_piece_value(board, color)
  sum_of_pieces_2 = compute_piece_value(board, OPPOSITE[color], True)

  return sum_of_pieces_1 - sum_of_pieces_2
