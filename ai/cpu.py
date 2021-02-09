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

def compute_piece_value(board, color, isUserWhite):
  sum_of_pieces = 0
  for piece in board[color].keys():
    y, x = board[color][piece]
    piece_name = piece.split('_')[0]
    piece_value = PIECE_VALUE[piece_name]
    piece_sq_values = PIECE_SQUARE_MAP[piece_name]
    if (isUserWhite and color == "white") or (not isUserWhite and color == "black"):
      piece_square_value = piece_sq_values[y][x]
    elif (isUserWhite and color == "black") or (not isUserWhite and color == "white"):
      piece_square_value = piece_sq_values[7 - y][7 - x]

    sum_of_pieces += (float(piece_value) + float(piece_square_value))
  return sum_of_pieces


def evaluate_board(board, isUserWhite):
  """
  evaluates the board using
   - piece values
   - piece square tables
  """
  color = "black" if isUserWhite else "white"
  if helper.in_checkmate(board, color):
    return float('-inf')
  if helper.in_checkmate(board, OPPOSITE[color]):
    return float('inf')

  sum_of_pieces_1 = compute_piece_value(board, color, isUserWhite)
  sum_of_pieces_2 = compute_piece_value(board, OPPOSITE[color], isUserWhite)

  return sum_of_pieces_1 - sum_of_pieces_2
