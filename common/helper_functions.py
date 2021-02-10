import copy

from common.constants import PIECE_VALUE, OPPOSITE
from common import rules


def game_over(board, color):
  if in_checkmate(board, color):
    return { "who_won": color, "by": "checkmate" }

  if in_checkmate(board, OPPOSITE[color]):
    return { "who_won": OPPOSITE[color], "by": "checkmate" }

  if in_stalemate(board, OPPOSITE[color]):
    return { "who_won": None, "by": "stalemate" }

  if is_draw(board):
    return { "who_won": None, "by": "draw" }

  return


def get_moves(board, color, filter_piece = None, isUserWhite = True):
  moves_list  = []
  moves = []

  for piece in board[color].keys():
    if "king" in piece:
      moves = rules.legal_king_moves(board, color, piece)
    elif "queen" in piece:
      moves = rules.legal_queen_moves(board, color, piece)
    elif "bishop" in piece:
      moves = rules.legal_bishop_moves(board, color, piece)
    elif "knight" in piece:
      moves = rules.legal_knight_moves(board, color, piece)
    elif "rook" in piece:
      moves = rules.legal_rook_moves(board, color, piece)
    elif "pawn" in piece:
      moves = rules.legal_pawn_moves(board, color, piece, isUserWhite=isUserWhite)

    for move in moves:
      moves_list = moves_list + [{"color": color, "piece": piece, "new_position": move}]

  return [move for move in moves_list if not filter_piece or move["piece"] == filter_piece]


def filter_moves_on_check(board, color, moves):
  if in_check(board, color):
    _moves = []
    for move in moves:
      clone_board = generate_board(board, move)
      if not in_check(clone_board, color):
        _moves.append(move)
    moves = _moves

  _moves = []
  for move in moves:
    clone_board = generate_board(board, move)
    if not in_check(clone_board, color):
      _moves.append(move)

  return _moves


def get_reverse_map(board):
  white = {}
  black = {}

  for k,v in board["white"].items():
    white[(v[0], v[1])]= k

  for k,v in board["black"].items():
    black[(v[0], v[1])]= k

  return { "white": white, "black": black }


def if_piece_under_attack(board, color, piece):
  oc = OPPOSITE[color]
  moves = []

  for x in board[oc].keys():
    if "king" in x:
      moves = moves + rules.legal_king_moves(board, oc, x)
    elif "queen" in x:
      moves = moves + rules.legal_queen_moves(board, oc, x)
    elif "bishop" in x:
      moves = moves + rules.legal_bishop_moves(board, oc, x)
    elif "knight" in x:
      moves = moves + rules.legal_knight_moves(board, oc, x)
    elif "rook" in x:
      moves = moves + rules.legal_rook_moves(board, oc, x)
    elif "pawn" in x:
      moves = moves + rules.legal_pawn_moves(board, oc, x)

  if board[color][piece] in moves:
    return True

  return False


def generate_board(board, move):
  new_board = copy.deepcopy(board)

  killed_piece = None
  for k, v in new_board[OPPOSITE[move['color']]].items():
    if move['new_position'] == v and k != "king":
      killed_piece = k

  if killed_piece and killed_piece in new_board[OPPOSITE[move['color']]].keys():
    del new_board[OPPOSITE[move['color']]][killed_piece]

  new_board[move['color']][move['piece']] = move['new_position']
  return new_board


def in_check(board, color):
  moves = get_moves(board, OPPOSITE[color])

  for move in moves:
    if board[color]['king'] == move['new_position']:
      return True

  return False


def checked_by(board, color):
  moves = get_moves(board, color)
  checking_pieces = []

  for move in moves:
    if board[color]['king'] == move['new_position']:
      checking_pieces.append(move["piece"])

  return checking_pieces


def in_checkmate(board, color):
  if in_check(board, color) is False:
    return False

  for move in get_moves(board, color):
    if in_check(generate_board(board, move), color) is False:
      return False

  return True


def in_stalemate(board, color_to_play):
  """If there are no moves for any of the armies and there is no check, it's a stalemate! """
  moves = get_moves(board, color_to_play)
  return len(moves) == 0 and in_check(board, color_to_play) is False


def is_draw(board):
  color = "white"
  num_pieces_1 = len(board[color].keys())
  num_pieces_2 = len(board[OPPOSITE[color]].keys())

  if num_pieces_1 > 2 or num_pieces_2 > 2:
    return False
  elif (
    num_pieces_1 <= 2 and (
      board[color].get("rook_1") or
      board[color].get("rook_2") or
      board[color].get("queen") or
      len([piece for piece in board[color].keys() if "pawn" in piece])
    )
  ):
      return False
  elif (
    board[OPPOSITE[color]].get("rook_1") or
    board[OPPOSITE[color]].get("rook_2") or
    board[OPPOSITE[color]].get("queen") or
    len([piece for piece in board[OPPOSITE[color]].keys() if "pawn" in piece])
  ):
    return False

  return True


def shielding(board, color, piece):
  """Shielding is how many pieces it's protecting from getting attacked, 
  one way to calculate it is if it's occupying a position which"""
    
  if piece not in board[color].keys():
    return 0.0

  clone_board = copy.deepcopy(board)
  del clone_board[color][piece]

  positions_with = set([(x['new_position'][0], x['new_position'][1]) for x in get_moves(board, OPPOSITE[color])])
  positions_without = set([(x['new_position'][0], x['new_position'][1]) for x in get_moves(clone_board, OPPOSITE[color])])

  positions_diff = positions_without - positions_with

  rboard = get_reverse_map(board)

  value  = 0.0

  """now if I remove the piece and try to find out what moves are possible.... 
  and then I put the piece back.. and find out what moves are possible... so the differece can show me 
  what pieces are actually being protected from this piece.."""
  for x in positions_diff:
    if x in rboard[color].keys():
      value += PIECE_VALUE[rboard[color][x]]

  return value
