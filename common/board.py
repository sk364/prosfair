from ai.alpha_beta_pruning import alpha_beta_pruning # _native as alpha_beta_pruning
from common import rules
from common.constants import BLACK, OPPOSITE, WHITE, DEPTH
from common.constants.pieces import PIECE_NAME_MAP, PIECE_PRIORITY_MAP, PIECE_SQUARE_MAP
from common.states.default import STATE as INITIAL_STATE


class Piece:
  def __init__(self, type, position, color):
    self.name = PIECE_NAME_MAP[type]
    self.type = type
    self.position = position
    self.color = color

  def __str__(self):
    return f'{self.name} [{self.color}] ({self.type}) - {self.position[0]}, {self.position[1]}'

  def __repr__(self):
    return f'{self.name} [{self.color}] ({self.type}) - {self.position[0]}, {self.position[1]}'

  def get_moves(self, board):
    return board.get_moves(self.color, filter_piece=self)

  def get_actual_position(self, user_color):
    """
    Returns standard chess board position (A2, H4, etc.)
    """
    y, x = self.position

    # flip values when user color is black as the board is flipped initially
    if user_color == BLACK:
      y, x = 7 - y, 7 - x

    return f'{chr(65 + x)}{8 - y}'

  def get_value(self, user_color):
    """
    Computes piece value by type and position using priority and square tables
    """
    y, x = self.position

    # flip values when user color is black as the board is flipped initially
    if user_color == BLACK:
      y, x = 7 - y, 7 - x

    return float(PIECE_PRIORITY_MAP[self.type]) + float(PIECE_SQUARE_MAP[self.type][y][x])

class Board:
  def __init__(self, user_color=WHITE):
    pieces = []
    for army, _pieces in INITIAL_STATE.items():
      for piece in _pieces:
        pieces.append(Piece(type=piece["type"], position=piece["position"], color=army))

    self.pieces = pieces
    self.user_color = user_color
    self.side_to_move = WHITE
    self.moves = []
    self.can_castle_king_side = True
    self.can_castle_queen_side = True

  def __str__(self):
    board_str = ""
    for row_idx in range(8):
      for col_idx in range(8):
        found = False
        for piece in self.pieces:
          if piece.position[1] == col_idx and piece.position[0] == row_idx:
            board_str += f'{piece.type} | '
            found = True
            break
        if not found:
          board_str += '  | '
      board_str += "\n"
    print(f'{self.side_to_move}:')
    print(board_str)
    print(", ".join([
      f'{move["piece"].type.upper()} ({move["piece"].get_actual_position(self.user_color)})'
      for move in self.moves
    ]))
    return ""

  def __repr__(self):
    return self.__str__()

  def flip(self):
    """Flips the board by updating each piece's position"""
    pieces = []
    for piece in self.pieces:
      y, x = piece.position
      y, x = 7 - y, 7 - x
      pieces.append(Piece(type=piece.type, position=[y, x], color=piece.color))
    self.pieces = pieces

  def clone(self, move=None):
    board = Board(user_color=self.user_color)
    board.pieces = [
      Piece(type=piece.type, position=piece.position, color=piece.color) for piece in self.pieces]

    if move:
      killed_piece_idx = None
      for idx, piece in enumerate(board.pieces):
        if piece.color == OPPOSITE[move["color"]] and piece.position == move['new_position']:
          killed_piece_idx = idx
          break

      if killed_piece_idx:
        del board.pieces[killed_piece_idx]

      for piece in board.pieces:
        if piece.color == move["color"] and piece.position == move["old_position"]:
          piece.position = move["new_position"]
          board._update_rook_position(piece, move)
          break

    return board

  def _update_rook_position(self, color, is_king_side):
    for _piece in self.pieces:
      if _piece.type == 'r':
        if self.user_color == color:
          if is_king_side and _piece.position == [7, 7]:
            _piece.position = [7, 5]
          if not is_king_side and _piece.position == [7, 0]:
            _piece.position = [7, 3]
        else:
          if is_king_side and _piece.position == [0, 7]:
            _piece.position = [0, 5]
          if not is_king_side and _piece.position == [0, 0]:
            _piece.position = 0, 3

  def _kill_pawn_on_en_passant(self, color, position):
    last_move = self.moves[-1] if len(self.moves) else None
    if not last_move or last_move["piece"].type != "p":
      return

    opp_color_positions = [piece.position for piece in self.pieces if piece.color != color]

    y, x = position
    if self.user_color == color:
      if y == 2:
        old_position, new_position = last_move["old_position"], last_move["new_position"]
        old_y, _ = old_position
        new_y, new_x = new_position
        if old_y == 1 and new_y == 3 and new_x == x and [2, x] not in opp_color_positions:
          killed_piece_idx = None
          for idx, piece in enumerate(self.pieces):
            if piece.type == "p" and piece.position == [3, x]:
              killed_piece_idx = idx
              break

          if killed_piece_idx is not None:
            del self.pieces[killed_piece_idx]
    elif y == 5:
      old_position, new_position = last_move["old_position"], last_move["new_position"]
      old_y, _ = old_position
      new_y, new_x = new_position
      if old_y == 6 and new_y == 4 and new_x == x and [5, x] not in opp_color_positions:
        killed_piece_idx = None
        for idx, piece in enumerate(self.pieces):
          if piece.type == "p" and piece.position == [4, x]:
            killed_piece_idx = idx
            break

        if killed_piece_idx is not None:
          del self.pieces[killed_piece_idx]

  def _promote_pawn(self, color, piece, upgrade_to="q"):
    pawn_idx = None
    for idx, _piece in enumerate(self.pieces):
      if _piece.type == piece.type and _piece.position == piece.position:
        pawn_idx = idx
        break

    if pawn_idx is not None:
      del self.pieces[pawn_idx]

    self.pieces.append(Piece(type=upgrade_to, color=piece.color, position=piece.position))

  def _update_position(self, move):
    for piece in self.pieces:
      if (
        piece.color == move["color"] and
        piece.type == move["piece"] and
        piece.position == move['old_position']
      ):
        piece.position = move['new_position']

        killed_piece_idx = None
        for idx, opp_piece in enumerate(self.pieces):
          if (
            opp_piece.color == OPPOSITE[self.side_to_move] and
            opp_piece.position == piece.position and
            opp_piece.type != "k"
          ):
            killed_piece_idx = idx
            break

        if killed_piece_idx is not None:
          del self.pieces[killed_piece_idx]

        if piece.type == "k":
          self.can_castle_king_side = False
          self.can_castle_queen_side = False
          num_steps_taken = piece.position[1] - move["old_position"][1]
          if abs(num_steps_taken) == 2:
            self._update_rook_position(self.side_to_move, num_steps_taken > 0)

        if piece.type == "r":
          if (self.side_to_move == self.user_color and move['old_position'] == [7, 7]) or (
            self.side_to_move != self.user_color and move['old_position'] == [0, 7]
          ):
            self.can_castle_king_side = False

          if (self.side_to_move == self.user_color and move['old_position'] == [7, 0]) or (
            self.side_to_move != self.user_color and move['old_position'] == [0, 0]
          ):
            self.can_castle_queen_side = False

        if piece.type == "p" and piece.position[0] in [0, 7]:
          self._promote_pawn(self.side_to_move, piece)

        self._kill_pawn_on_en_passant(self.side_to_move, move["new_position"])

        self.moves.append({ **move, "piece": piece })
        self.__str__()

        self.side_to_move = OPPOSITE[self.side_to_move]

        return self.game_over()
    return

  def play_move(self, move=None):
    if self.side_to_move != self.user_color and move is None:
      move = alpha_beta_pruning(self, self.side_to_move, DEPTH)
    return self._update_position(move)

  def in_check(self, color):
    """
    `color` army is in check if the `color`'s king is in any of the opposite army's moves
    """
    moves = [move['new_position'] for move in self.get_moves(OPPOSITE[color])]

    for move in moves:
      for piece in self.pieces:
        if piece.color == color and piece.type == "k" and piece.position in moves:
          return True

    return False

  def in_checkmate(self, color=None):
    if not color:
      color = self.side_to_move

    if self.in_check(color) is False:
      return False

    for move in self.get_moves(color):
      board = self.clone(move=move)
      if board.in_check(color) is False:
        return False

    return True

  def in_stalemate(self):
    """If there are no moves for any of the armies and there is no check, it's a stalemate!"""
    moves = self.get_moves(self.side_to_move)
    return len(moves) == 0 and self.in_check(self.side_to_move) is False

  def in_draw(self):
    color = WHITE

    color_pieces = [piece for piece in self.pieces if piece.color == color]
    opp_color_pieces = [piece for piece in self.pieces if piece.color == OPPOSITE[color]]

    num_pieces_1 = len(color_pieces)
    num_pieces_2 = len(opp_color_pieces)

    if num_pieces_1 > 2 or num_pieces_2 > 2:
      return False

    for piece in self.pieces:
      if piece.type == "r" or piece.type == "q" or piece.type == "p":
        return False

    return True

  def game_over(self):
    if self.in_checkmate():
      return { "who_won": self.side_to_move, "by": "checkmate" }

    if self.in_stalemate():
      return { "who_won": None, "by": "stalemate" }

    if self.in_draw():
      return { "who_won": None, "by": "draw" }

    return

  def get_moves(self, color, filter_piece=None):
    pieces = [piece for piece in self.pieces if piece.color == color]
    moves = []

    for piece in pieces:
      if piece.type == "p":
        legal_moves = rules.legal_pawn_moves
      if piece.type == "b":
        legal_moves = rules.legal_bishop_moves
      if piece.type == "n":
        legal_moves = rules.legal_knight_moves
      if piece.type == "k":
        legal_moves = rules.legal_king_moves
      if piece.type == "q":
        legal_moves = rules.legal_queen_moves
      if piece.type == "r":
        legal_moves = rules.legal_rook_moves

      if filter_piece is None or (
        piece.type == filter_piece.type and
        piece.position == filter_piece.position and
        piece.color == filter_piece.color
      ):
        moves += [
          {"color": color, "piece": piece.type, "old_position": piece.position, "new_position": move}
          for move in legal_moves(self, color, piece.position)
        ]
    return moves

  def filter_moves_on_check(self, color, moves):
    """
    Filters moves preventing check
    """
    if self.in_check(color):
      _moves = []
      for move in moves:
        board = self.clone(move)
        if not board.in_check(color):
          _moves.append(move)

      moves = _moves

    return moves
