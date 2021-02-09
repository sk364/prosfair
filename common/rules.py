import json
from common.constants import OPPOSITE


def legal_king_moves(board, color, king='king'):
  if king not in board[color].keys():
    return []

  x, y = board[color][king] 

  king_moves = []
  for i in range(3):
    for j in range(3):
      if  8 > x + i - 1 > -1 and 8 > y + j- 1 > -1:
        if x + i- 1 != x or y + j- 1 != y:
          king_moves  = king_moves +  [[x + i- 1, y + j- 1]] 

  return [ x for x in king_moves if x not in board[color].values() ]


def legal_pawn_moves(board, color, pawn, isUserWhite = True):
  if pawn not in board[color].keys():
    return []

  x, y = board[color][pawn]

  pawn_moves = []
  if (isUserWhite and color == "black") or (not isUserWhite and color == "white"):
    if x == 1:
      if 8 > y > -1:
        if [x + 2, y] not in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x + 2, y]]
    if x < 7:
      if 8 > y > -1:
        if [x + 1, y] not in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x + 1, y]]
      if y > 0:
        if [x + 1, y - 1] in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x + 1, y - 1]]
      if y < 7:
        if [x + 1, y + 1] in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x + 1, y + 1]]
  elif (isUserWhite and color == "white") or (not isUserWhite and color == "black"):
    if x == 6:
      if 8 > y > -1:
        if [x - 2, y] not in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x - 2, y]]
    if x > 0:
      if 8 > y > -1:
        if [x - 1, y] not in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x - 1, y]]
      if y > 0:
        if [x - 1, y - 1] in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x - 1, y - 1]]
      if y < 7:
        if [x - 1, y + 1] in board[OPPOSITE[color]].values():
          pawn_moves = pawn_moves + [[x - 1, y + 1]]

  return [x for x in pawn_moves if x not in board[color].values()]


def legal_bishop_moves(board,color,bishop):
  if bishop not in board[color].keys():
    return []

  x, y = board[color][bishop]

  bishop_moves = []
  for i in range(8):
    if x - i - 1 > -1 and y + i + 1 < 8:
      if [x - i - 1, y + i + 1] in board[color].values():
        break
      bishop_moves = bishop_moves + [[x - i - 1, y + i + 1]]
      if [x - i - 1, y + i + 1] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if x - i - 1 > -1 and y - i - 1 > -1:
      if [x - i - 1, y - i - 1] in board[color].values():
        break
      bishop_moves = bishop_moves + [[x - i - 1, y - i - 1]]
      if [x - i - 1, y - i - 1] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if x + i + 1 < 8 and y - i - 1 > -1:
      if [x + i + 1, y - i - 1] in board[color].values():
        break
      bishop_moves = bishop_moves + [[x + i + 1, y - i - 1]]
      if [x + i + 1, y - i - 1] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if x + i + 1 < 8 and y + i + 1 < 8:
      if [x + i + 1, y + i + 1] in board[color].values():
        break
      bishop_moves = bishop_moves + [[x + i + 1, y + i + 1]]
      if [x + i + 1, y + i + 1] in board[OPPOSITE[color]].values():
        break

  return [x for x in bishop_moves if x not in board[color].values()]


def legal_knight_moves(board, color, knight):
  if knight not in board[color].keys():
    return []

  x, y = board[color][knight]
  knight_moves = []
  if x + 2 < 8 and y + 1 < 8:
    knight_moves = knight_moves + [[x + 2, y + 1]]

  if x + 1 < 8 and y + 2 < 8:
    knight_moves = knight_moves + [[x + 1, y + 2]]

  if x - 1 > -1 and y + 2 < 8:
    knight_moves = knight_moves + [[x - 1, y + 2]]
  
  if x - 1 > -1 and y - 2 > -1:
    knight_moves = knight_moves + [[x - 1, y - 2]]

  if x + 2 < 8 and y - 1 > -1:
    knight_moves = knight_moves + [[x + 2, y - 1]]

  if x + 1 < 8 and y - 2 > -1:
    knight_moves = knight_moves + [[x + 1, y - 2]]

  if x - 2 > -1 and y - 1 > -1:
    knight_moves = knight_moves + [[x - 2, y - 1]]

  if x - 2 > -1 and y + 1 < 8:
    knight_moves = knight_moves + [[x - 2, y + 1]]   

  return [x for x in knight_moves if x not in board[color].values()]


def legal_rook_moves(board,color,rook):
  if rook not in board[color].keys():
    return []

  x, y = board[color][rook]

  rook_moves = []
  for i in range(8):
    if x + i + 1 < 8:
      if [x + i + 1, y] in board[color].values():
        break
      rook_moves = rook_moves + [[x + i + 1, y]]
      if [x + i + 1, y] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if x - i - 1 > -1:
      if [x - i - 1, y] in board[color].values():
        break
      rook_moves = rook_moves + [[x - i - 1,y]]
      if [x - i - 1, y] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if y + i + 1 < 8:
      if [x,y + i + 1] in board[color].values():
        break
      rook_moves = rook_moves + [[x, y + i + 1]]
      if [x, y + i + 1] in board[OPPOSITE[color]].values():
        break

  for i in range(8):
    if y - i - 1 > -1:
      if [x, y - i - 1] in board[color].values():
        break
      rook_moves = rook_moves + [[x, y - i - 1]]
      if [x, y - i - 1] in board[OPPOSITE[color]].values():
        break
  
  return [x for x in rook_moves if x not in board[color].values()]


def legal_queen_moves(board, color,queen="queen"):
  if queen not in board[color].keys():
    return []

  x, y = board[color][queen]
  queen_moves = legal_rook_moves(board, color, queen) + legal_bishop_moves(board, color, queen)
  return [x for x in queen_moves if x not in board[color].values()]
