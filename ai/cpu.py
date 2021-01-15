import json
import subprocess

from common import helper_functions as helper


def emperical_comparision(board, color):
  return sum(
    [ float(piece_value[piece]) for piece in board[color].keys() ]
  ) - sum(
    [ float(piece_value[piece]) for piece in board[opposite[color]].keys() ]
  )


def risk_comparision(board, color):
  return sum(
    [ float(piece_value[piece]) for piece in board[opposite[color]].keys()
      if helper.if_piece_under_attack(board, opposite[color], piece) ]
  ) - sum(
    [ float(piece_value[piece]) for piece in board[color].keys() if helper.if_piece_under_attack(board, color, piece) ]
  )


def defence_comparision(board, color):
  return sum(
    [ float(helper.shielding(board, color, piece)) for piece in board[color].keys() ]
  ) - sum (
    [ float(helper.shielding(board, opposite[color], piece)) for piece in board[opposite[color]].keys() ]
  )


def evaluate_board(board, color):
  if helper.in_checkmate(board, color) or helper.in_check(board, color):
    return float('-inf')
  if helper.in_checkmate(board, opposite[color]) or helper.in_check(board, opposite[color]):
    return float('inf')
  ##TODO: here only two epiecetremes cases has only been handled
  ##      need to write the middle cases, which will include
  ##  the current position of the player's pieces.

  emperical_eval = emperical_comparision(board, color) 
  risk_eval      = risk_comparision(board, color)
  defence_eval   = defence_comparision(board, color)
  
  #print emperical_eval , risk_eval  , defence_eval 
  
  return risk_eval
