def legal_king_moves(board, color, position):
  y, x = position

  color_positions = [piece.position for piece in board.pieces if piece.color == color]

  moves = []
  for i in range(3):
    for j in range(3):
      if  8 > y + i - 1 > -1 and 8 > x + j - 1 > -1:
        if y + i - 1 != x or x + j - 1 != x:
          moves += [[y + i - 1, x + j - 1]]

  if board.can_castle_king_side:
    if [y, x + 1] not in color_positions and [y, x + 2] not in color_positions:
      moves += [[y, x + 2]]

  if board.can_castle_queen_side:
    can_castle = True
    for i in range(3):
      if [y, x - i] in color_positions:
        can_castle = False
    if can_castle:
      moves += [[y, x - 2]]

  moves = [move for move in moves if move not in color_positions]
  return moves


def legal_pawn_moves(board, color, position):
  y, x = position

  opp_color_positions = [piece.position for piece in board.pieces if piece.color != color]
  color_positions = [piece.position for piece in board.pieces if piece.color == color]
  last_move = board.moves[-1] if len(board.moves) else None

  moves = []
  if board.user_color != color:
    if y == 1:
      if 8 > x > -1:
        if (
          [y + 2, x] not in opp_color_positions and
          [y + 1, x] not in opp_color_positions and
          [y + 1, x] not in color_positions
        ):
          moves += [[y + 2, x]]
    if y < 7:
      if 8 > x > -1:
        if [y + 1, x] not in opp_color_positions:
          moves += [[y + 1, x]]
      if x > 0:
        if [y + 1, x - 1] in opp_color_positions:
          moves += [[y + 1, x - 1]]
      if x < 7:
        if [y + 1, x + 1] in opp_color_positions:
          moves += [[y + 1, x + 1]]

    if last_move and y == 4 and last_move["piece"].type == "p":
      old_position, new_position = last_move["old_position"], last_move["new_position"]
      old_y, _ = old_position
      new_y, new_x = new_position
      if old_y == 6 and new_y == 4:
        if new_x == x - 1:
          moves += [[y + 1, x - 1]]
        elif new_x == x + 1:
          moves += [[y + 1, x + 1]]
  else:
    if y == 6:
      if 8 > x > -1:
        if (
          [y - 2, x] not in opp_color_positions and
          [y - 1, x] not in opp_color_positions and
          [y - 1, x] not in color_positions
        ):
          moves += [[y - 2, x]]
    if y > 0:
      if 8 > x > -1:
        if [y - 1, x] not in opp_color_positions:
          moves += [[y - 1, x]]
      if x > 0:
        if [y - 1, x - 1] in opp_color_positions:
          moves += [[y - 1, x - 1]]
      if x < 7:
        if [y - 1, x + 1] in opp_color_positions:
          moves += [[y - 1, x + 1]]

    if last_move and y == 3 and last_move["piece"].type == "p":
      old_position, new_position = last_move["old_position"], last_move["new_position"]
      old_y, _ = old_position
      new_y, new_x = new_position
      if old_y == 1 and new_y == 3:
        if new_x == x - 1:
          moves += [[y - 1, x - 1]]
        elif new_x == x + 1:
          moves += [[y - 1, x + 1]]

  return [move for move in moves if move not in color_positions]


def legal_bishop_moves(board, color, position):
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


def legal_knight_moves(board, color, position):
  y, x = position

  color_positions = [piece.position for piece in board.pieces if piece.color == color]

  moves = []
  if y + 2 < 8 and x + 1 < 8:
    moves += [[y + 2, x + 1]]

  if y + 1 < 8 and x + 2 < 8:
    moves += [[y + 1, x + 2]]

  if y - 1 > -1 and x + 2 < 8:
    moves += [[y - 1, x + 2]]
  
  if y - 1 > -1 and x - 2 > -1:
    moves += [[y - 1, x - 2]]

  if y + 2 < 8 and x - 1 > -1:
    moves += [[y + 2, x - 1]]

  if y + 1 < 8 and x - 2 > -1:
    moves += [[y + 1, x - 2]]

  if y - 2 > -1 and x - 1 > -1:
    moves += [[y - 2, x - 1]]

  if y - 2 > -1 and x + 1 < 8:
    moves += [[y - 2, x + 1]]   

  return [move for move in moves if move not in color_positions]


def legal_rook_moves(board, color, position):
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


def legal_queen_moves(board, color, position):
  color_positions = [piece.position for piece in board.pieces if piece.color == color]
  moves = (
    legal_rook_moves(board, color, position) +
    legal_bishop_moves(board, color, position)
  )
  return [move for move in moves if move not in color_positions]
