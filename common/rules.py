from common.constants import OPPOSITE


def legal_king_moves(board, color, position, **kwargs):
  """
  Returns legal king moves looking up it's eight neighbouring blocks, adding in castling move if
  king and king/queen side rooks are at their initial positions and there is no attack on the
  either of the two blocks on either side of the king
  """

  y, x = position

  color_positions = [piece.position for piece in board.pieces if piece.color == color]
  if not kwargs.get('is_opposition'):
    # these moves help determine if the king can castle or not
    opp_color_moves = board.get_moves(OPPOSITE[color], filter_piece=None, is_opposition=True)
  else:
    opp_color_moves = []

  moves = []
  for i in range(3):
    for j in range(3):
      if 8 > y + i - 1 > -1 and 8 > x + j - 1 > -1 and (y + i - 1 != x or x + j - 1 != x):
        moves += [[y + i - 1, x + j - 1]]

  if board.can_castle_king_side:
    if (
      [y, x + 1] not in color_positions and
      [y, x + 2] not in color_positions and
      [y, x + 1] not in opp_color_moves and
      [y, x + 2] not in opp_color_moves
    ):
      moves += [[y, x + 2]]

  if board.can_castle_queen_side:
    can_castle = True
    for i in range(3):
      if [y, x - i] in color_positions and (i != 2 and [y, x - i] not in opp_color_moves):
        can_castle = False

    if can_castle:
      moves += [[y, x - 2]]

  return [move for move in moves if move not in color_positions]


def legal_pawn_moves(board, color, position, **kwargs):
  """
  Returns legal pawns computing if it can move:
  one block / two block / killing move / en-passant move
  based on opposite side positions and the last move played by it
  """

  y, x = position

  opp_color_positions = [piece.position for piece in board.pieces if piece.color != color]
  color_positions = [piece.position for piece in board.pieces if piece.color == color]
  last_move = board.moves[-1] if len(board.moves) else None

  if board.user_color != color:
    # flip coordinates as if facing the user
    y, x = 7 - y, 7 - x
    opp_color_positions = [[7 - pos[0], 7 - pos[1]] for pos in opp_color_positions]
    color_positions = [[7 - pos[0], 7 - pos[1]] for pos in color_positions]

  moves = []

  if y == 6:
    # on initial position, check if pawn can jump over 2 blocks
    if 8 > x > -1:
      if (
        [y - 2, x] not in opp_color_positions and
        [y - 1, x] not in opp_color_positions and
        [y - 1, x] not in color_positions
      ):
        moves += [[y - 2, x]]

  if y > 0:
    # pawn can move one block ahead if there is no opponent piece on it
    if 8 > x > -1 and [y - 1, x] not in opp_color_positions:
      moves += [[y - 1, x]]

    # pawn can kill if there is an opponent piece on its left or right diagonal block
    if x > 0 and [y - 1, x - 1] in opp_color_positions:
      moves += [[y - 1, x - 1]]
    if x < 7 and [y - 1, x + 1] in opp_color_positions:
      moves += [[y - 1, x + 1]]

  # pawn can kill en-passant if the last move played by opposition is a pawn and it jumped two
  # blocks by the side of this pawn
  if last_move and last_move["piece"].type == "p" and y == 3:
    old_position, new_position = last_move["old_position"], last_move["new_position"]
    old_y, _ = old_position
    new_y, new_x = new_position

    if board.user_color != color:
      old_y = 7 - old_y
      new_y, new_x = 7 - new_y, 7 - new_x

    if old_y == 1 and new_y == 3:
      if new_x == x - 1:
        moves += [[y - 1, x - 1]]
      elif new_x == x + 1:
        moves += [[y - 1, x + 1]]

  moves = [move for move in moves if move not in color_positions]

  if board.user_color != color:
    # re-flip the above flipped coordinates
    return [[7 - move[0], 7 - move[1]] for move in moves]

  return moves


def legal_bishop_moves(board, color, position, **kwargs):
  """
  Returns legal bishop moves looking over positions of its own and opposition's piece over
  the two diagonals
  """

  y, x = position

  opp_color_positions = [piece.position for piece in board.pieces if piece.color != color]
  color_positions = [piece.position for piece in board.pieces if piece.color == color]

  moves = []
  for i in range(8):
    if y - i - 1 > -1 and x + i + 1 < 8:
      if [y - i - 1, x + i + 1] in color_positions:
        break

      moves += [[y - i - 1, x + i + 1]]

      if [y - i - 1, x + i + 1] in opp_color_positions:
        break

  for i in range(8):
    if y - i - 1 > -1 and x - i - 1 > -1:
      if [y - i - 1, x - i - 1] in color_positions:
        break

      moves += [[y - i - 1, x - i - 1]]

      if [y - i - 1, x - i - 1] in opp_color_positions:
        break

  for i in range(8):
    if y + i + 1 < 8 and x - i - 1 > -1:
      if [y + i + 1, x - i - 1] in color_positions:
        break

      moves += [[y + i + 1, x - i - 1]]

      if [y + i + 1, x - i - 1] in opp_color_positions:
        break

  for i in range(8):
    if y + i + 1 < 8 and x + i + 1 < 8:
      if [y + i + 1, x + i + 1] in color_positions:
        break

      moves += [[y + i + 1, x + i + 1]]

      if [y + i + 1, x + i + 1] in opp_color_positions:
        break

  return [move for move in moves if move not in color_positions]


def legal_knight_moves(board, color, position, **kwargs):
  """
  Returns legal knight moves looking over all eight positions 2 and a half blocks from it
  """

  y, x = position

  color_positions = [piece.position for piece in board.pieces if piece.color == color]

  moves = []
  for idx in range(2):
    i, j = [1, 2] if idx == 0 else [2, 1]
    if y + i < 8:
      if x + j < 8:
        moves += [[y + i, x + j]]
      if x - j > -1:
        moves += [[y + i, x - j]]
    if y - i > -1:
      if x + j < 8:
        moves += [[y - i, x + j]]
      if x - j > -1:
        moves += [[y - i, x - j]]

  return [move for move in moves if move not in color_positions]


def legal_rook_moves(board, color, position, **kwargs):
  """
  Returns legal rook moves, looking up horizontally and vertically positions of its own and
  opposition pieces
  """

  y, x = position

  opp_color_positions = [piece.position for piece in board.pieces if piece.color != color]
  color_positions = [piece.position for piece in board.pieces if piece.color == color]

  moves = []
  for i in range(8):
    if y + i + 1 < 8:
      if [y + i + 1, x] in color_positions:
        break

      moves += [[y + i + 1, x]]

      if [y + i + 1, x] in opp_color_positions:
        break

  for i in range(8):
    if y - i - 1 > -1:
      if [y - i - 1, x] in color_positions:
        break

      moves += [[y - i - 1, x]]

      if [y - i - 1, x] in opp_color_positions:
        break

  for i in range(8):
    if x + i + 1 < 8:
      if [y, x + i + 1] in color_positions:
        break

      moves += [[y, x + i + 1]]

      if [y, x + i + 1] in opp_color_positions:
        break

  for i in range(8):
    if x - i - 1 > -1:
      if [y, x - i - 1] in color_positions:
        break

      moves += [[y, x - i - 1]]

      if [y, x - i - 1] in opp_color_positions:
        break

  return [move for move in moves if move not in color_positions]


def legal_queen_moves(board, color, position, **kwargs):
  """
  Returns moves combining legal rook and bishop moves
  """

  color_positions = [piece.position for piece in board.pieces if piece.color == color]
  moves = (
    legal_rook_moves(board, color, position) +
    legal_bishop_moves(board, color, position)
  )
  return [move for move in moves if move not in color_positions]
