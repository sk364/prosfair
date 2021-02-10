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

def get_pawn_counts(board, color, isUserWhite):
  """
  computes number of doubled, isolated, blocked and connected pawns for a side
  """

  own_army_positions = board[color].values()
  opposite_army_positions = board[OPPOSITE[color]].values()

  own_pawn_positions = []
  opposite_pawn_positions = []
  for idx in range(8):
    own_pawn_position = board[color].get(f"pawn_{idx + 1}")
    opposite_pawn_position = board[OPPOSITE[color]].get(f"pawn_{idx + 1}")
    if own_pawn_position:
      own_pawn_positions.append(own_pawn_position)
    if opposite_pawn_position:
      opposite_pawn_positions.append(opposite_pawn_position)

  pawn_counts = {
    "doubled": 0,
    "blocked": 0,
    "isolated": 0,
    "connected": 0
  }
  pieces = board[color]

  for idx in range(8):
    pawn_key = f"pawn_{idx + 1}"
    position = pieces.get(pawn_key)
    if not position:
      continue

    y, x = position

    if (color == "black" and isUserWhite) or (color == "white" and not isUserWhite):
      if [y + 1, x] in opposite_army_positions:
        if (
          [y + 1, x + 1] not in opposite_army_positions and
          [y + 1, x - 1] not in opposite_army_positions
        ):
          pawn_counts["blocked"] += 1
    elif (color == "black" and not isUserWhite) or (color == "white" and isUserWhite):
      if [y - 1, x] in opposite_army_positions:
        if (
          [y - 1, x + 1] not in opposite_army_positions and
          [y - 1, x - 1] not in opposite_army_positions
        ):
          pawn_counts["blocked"] += 1

    if [y + 1, x] in own_pawn_positions or [y - 1, x] in own_pawn_positions:
      pawn_counts["doubled"] += 1

    if (
      [y + 1, x + 1] not in own_pawn_positions and
      [y + 1, x - 1] not in own_pawn_positions and
      [y - 1, x + 1] not in own_pawn_positions and
      [y - 1, x - 1] not in own_pawn_positions and
      [y, x - 1] not in own_pawn_positions and
      [y, x + 1] not in own_pawn_positions and
      [y + 1, x] not in own_pawn_positions and
      [y - 1, x] not in own_pawn_positions
    ):
      pawn_counts["isolated"] += 1
    else:
      pawn_counts["connected"] += 1
  return pawn_counts


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


def compute_mobility(board, color, isUserWhite):
  """
  returns number of valid positions for a side
  """
  return len(helper.get_moves(board, color, filter_piece=None, isUserWhite=isUserWhite))


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
  pawn_counts_1 = get_pawn_counts(board, color, isUserWhite)
  pawn_counts_2 = get_pawn_counts(board, OPPOSITE[color], isUserWhite)
  mobility_1 = compute_mobility(board, color, isUserWhite)
  mobility_2 = compute_mobility(board, OPPOSITE[color], isUserWhite)

  score = (
    (sum_of_pieces_1 - sum_of_pieces_2) -
    (
      0.5 * (
        (pawn_counts_1["doubled"] - pawn_counts_2["doubled"]) +
        (pawn_counts_1["blocked"] - pawn_counts_2["doubled"]) +
        (pawn_counts_1["isolated"] - pawn_counts_2["isolated"])
      )
    ) +
    0.1 * (mobility_1 - mobility_2)
  )

  return score
