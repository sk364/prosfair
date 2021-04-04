import subprocess
import time

from collections import defaultdict

from ai.cpu import evaluate_board
from common.constants import OPPOSITE, BLACK


def transform_board_to_string(board):
  """
  Transforms board piece positions into line-separated "<y> <x>" strings
  """

  data = ""
  piece_order = ["k", "q", "b", "n", "r", "p"]
  piece_codes = ["k", "q", "b", "b", "n", "n", "r", "r", "p", "p", "p", "p", "p", "p", "p", "p"]

  user_piece_positions = {
    "k": [],
    "q": [],
    "b": [],
    "n": [],
    "r": [],
    "p": []
  }
  cpu_piece_positions = {
    "k": [],
    "q": [],
    "b": [],
    "n": [],
    "r": [],
    "p": []
  }
  user_pieces = [_p for _p in board.pieces if _p.color == board.user_color]
  cpu_pieces = [_p for _p in board.pieces if _p.color != board.user_color]

  for piece in user_pieces:
    user_piece_positions[piece.type].append(piece.position)

  for piece_type in piece_order:
    positions = user_piece_positions[piece_type]
    if piece_type == 'k' or piece_type == 'q':
      if positions:
        data += f'{positions[0][0]} {positions[0][1]}\n'
      else:
        data += '-1 1\n'
    else:
      if piece_type in ['b', 'n', 'r']:
        num_killed = 2 - len(positions)
      else:
        num_killed = 8 - len(positions)

      for position in positions:
        data += f'{position[0]} {position[1]}\n'

      for _ in range(num_killed):
        data += '-1 1\n'

  for piece in cpu_pieces:
    cpu_piece_positions[piece.type].append(piece.position)

  for piece_type in piece_order:
    positions = cpu_piece_positions[piece_type]
    if piece_type == 'k' or piece_type == 'q':
      if positions:
        data += f'{positions[0][0]} {positions[0][1]}\n'
      else:
        data += '-1 1\n'
    else:
      if piece_type in ['b', 'n', 'r']:
        num_killed = 2 - len(positions)
      else:
        num_killed = 8 - len(positions)

      for position in positions:
        data += f'{position[0]} {position[1]}\n'

      for _ in range(num_killed):
        data += '-1 1\n'

  return data


def alpha_beta_pruning(board, color, depth):
  """
  Returns the best move calculated using the C++ compiled binary
  """

  st = time.time()

  player = 16
  proc = subprocess.Popen(
    ["ai/minimax", str(player), str(depth)],
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE
  )
  data = transform_board_to_string(board)
  out = proc.communicate(data.encode("utf-8"))
  total = time.time() - st

  old_pos, piece, x, y, score = out[0].decode('utf-8').split(" ")
  piece = piece_codes[int(piece) - player]
  x, y, old_pos = int(x), int(y), int(old_pos)
  old_y, old_x = [old_pos // 8, old_pos % 8]

  if player == 0:
    y, x = 7 - y, 7 - x
    old_y, old_x = 7 - old_y, 7 - old_x

  move = {'color': color, 'piece': piece, 'new_position': [y, x], 'old_position': [old_y, old_x]}

  print(total)
  print(out[0].decode('utf-8').split(" "))
  print(move, score)

  return move


def alpha_beta_pruning_native(board, color, depth):
  """
  Returns the best move using Pythonic alpha-beta optimized minimax implementation
  """

  print("Calculating...")
  st = time.time()

  score_cache = defaultdict()
  moves_list = board.get_moves(color)

  if len(moves_list) == 0 or depth == 0:
    return None

  best_move = moves_list[0]
  best_score = float('-inf')

  alpha = float('-inf')
  beta = float('inf')

  for move in moves_list:
    clone_board = board.clone(move)
    score = alpha_beta_min(clone_board, OPPOSITE[color], alpha, beta, depth - 1, score_cache)
    if score > best_score:
      best_move = move
      best_score = score

  total = time.time() - st
  print(total)
  print(best_move, best_score)

  from pprint import pprint
  pprint(score_cache)

  return best_move


def alpha_beta_min(board, color, alpha, beta, depth, score_cache):
  if depth == 0:
    board_str = transform_board_to_string(board)
    if score_cache.get(board_str) is None:
      score_cache[board_str] = evaluate_board(board)

    return score_cache[board_str]

  moves_list = board.get_moves(color)

  for move in moves_list:
    clone_board = board.clone(move)

    score = alpha_beta_max(clone_board, OPPOSITE[color], alpha, beta, depth - 1, score_cache)

    if score <= alpha:
      board_str = transform_board_to_string(clone_board)
      score_cache[board_str] = alpha
      return score_cache[board_str]

    if score < beta:
      beta = score

  board_str = transform_board_to_string(board)
  score_cache[board_str] = beta
  return score_cache[board_str]


def alpha_beta_max(board, color, alpha, beta, depth, score_cache):
  if depth == 0:
    board_str = transform_board_to_string(board)
    if score_cache.get(board_str) is None:
      score_cache[board_str] = -evaluate_board(board)

    return score_cache[board_str]

  moves_list = board.get_moves(color)

  for move in moves_list:
    clone_board = board.clone(move)

    score = alpha_beta_min(clone_board, OPPOSITE[color], alpha, beta, depth - 1, score_cache)

    if score >= beta:
      board_str = transform_board_to_string(clone_board)
      score_cache[board_str] = beta
      return score_cache[board_str]

    if score > alpha:
      alpha = score

  board_str = transform_board_to_string(board)
  score_cache[board_str] = alpha
  return score_cache[board_str]
