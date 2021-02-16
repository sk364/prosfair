import subprocess
import time

from ai.cpu import evaluate_board
from common.constants import OPPOSITE, BLACK


def alpha_beta_pruning(board, color, depth):
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
  user_pieces = [_p for _p in board.pieces if _p.color != color]
  cpu_pieces = [_p for _p in board.pieces if _p.color == color]

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

  player = 16 if color == BLACK else 0

  proc = subprocess.Popen(
    ["ai/minimax", str(player), str(depth)],
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE
  )

  st = time.time()
  out = proc.communicate(data.encode("utf-8"))
  total = time.time() - st
  print(total)

  old_pos, piece, x, y = out[0].decode('utf-8').split(" ")
  piece = piece_codes[int(piece) - player]
  x, y, old_pos = int(x), int(y), int(old_pos)
  old_y, old_x = [old_pos // 8, old_pos % 8]

  if player == 0:
    y, x = 7 - y, 7 - x
    old_y, old_x = 7 - old_y, 7 - old_x

  move = {'color': color, 'piece': piece, 'new_position': [y, x], 'old_position': [old_y, old_x]}
  print(move)

  return move


def alpha_beta_pruning_native(board, color, depth):
  print("Calculating...")
  st = time.time()
  moves_list = board.get_moves(color)
  moves_list = board.filter_moves_on_check(color, moves_list)

  if len(moves_list) == 0 or depth == 0:
    return None

  best_move = moves_list[0]
  best_score = float('-inf')

  alpha = float('-inf')
  beta = float('inf')

  for move in moves_list:
    clone_board = board.clone(move)
    score = alpha_beta(
      clone_board, OPPOSITE[color], alpha, beta, depth - 1, is_min=True)
    if score > best_score:
      best_move = move
      best_score = score

  total = time.time() - st
  print(total)
  print(best_move, best_score)

  return best_move


def alpha_beta(board, color, alpha, beta, depth, is_min = False):
  if depth == 0:
    return (-1 if is_min else 1) * evaluate_board(board)

  moves_list = board.get_moves(color)
  moves_list = board.filter_moves_on_check(color, moves_list)

  score = float('inf') if is_min else float('-inf')
  for move in moves_list:
    clone_board = board.clone(move)
    if not is_min:
      score = max(score, alpha_beta(
        clone_board, OPPOSITE[color], alpha, beta, depth - 1, is_min=True))
      alpha = max(alpha, score)
      if beta <= alpha:
        return score
    else:
      score = min(score, alpha_beta(
        clone_board, OPPOSITE[color], alpha, beta, depth - 1, is_min=False))
      beta = min(beta, score)
      if beta <= alpha:
        return score

  return score
