from ai.alpha_beta_pruning import alpha_beta_pruning_native as alpha_beta_pruning
from common.constants import BLACK, OPPOSITE, WHITE, DEPTH
from common.constants.pieces import (
  PIECE_NAME_MAP,
  PIECE_PRIORITY_MAP,
  PIECE_SQUARE_MAP,
  PIECE_RULE_METHODS
)
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
            board_str += f'{piece.type if piece.color == self.side_to_move else piece.type.upper()} | '
            found = True
            break
        if not found:
          board_str += '  | '
      board_str += "\n"
    print(f'{self.side_to_move}:')
    print(board_str)
    print(", ".join([
      f'{move["piece"].type.upper()} ({move["piece"].get_actual_position(self.side_to_move)})'
      for move in self.moves
    ]))
    return ""

  def __repr__(self):
    return str(self)

  def flip(self):
    """Flips the board by updating each piece's position"""
    pieces = []
    for piece in self.pieces:
      y, x = piece.position
      y, x = 7 - y, 7 - x
      pieces.append(Piece(type=piece.type, position=[y, x], color=piece.color))
    self.pieces = pieces

  def clone(self, move=None):
    """
    Clones the board, optionally simulating a move, if provided
    """

    board = Board(user_color=self.user_color)
    board.side_to_move = self.side_to_move
    board.pieces = [
      Piece(type=piece.type, position=piece.position, color=piece.color)
      for piece in self.pieces
    ]

    if move:
      board._update_position(move, is_clone_board=True)

    return board

  def _kill_piece_if_any(self, piece):
    """
    Removes opponent piece from the board if the current piece in consideration is on its position
    """

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

  def _update_rook_position(self, color, is_king_side):
    """
    Updates rook position when king has castled to either king/queen side
    """

    for _piece in self.pieces:
      if _piece.type == 'r':
        pos = 7 if self.user_color == color else 0
        if is_king_side and _piece.position == [pos, 7]:
          _piece.position = [pos, 5]
        if not is_king_side and _piece.position == [pos, 0]:
          _piece.position = [pos, 3]

  def _kill_pawn_on_en_passant(self, last_move, color, position):
    """
    Removes the opponent's pawn if it is killed by "en-passant"
    """

    opp_color_positions = [piece.position for piece in self.pieces if piece.color != color]

    y, x = position
    old_position, new_position = last_move["old_position"], last_move["new_position"]
    old_y, _ = old_position
    new_y, new_x = new_position
    pos = 3
    opp_pos = 2
    if self.user_color != color:
      y = 7 - y
      old_y = 7 - old_y
      new_y = 7 - new_y
      pos = 7 - pos
      opp_pos = 7 - opp_pos

    if old_y == 1 and new_y == 3 and new_x == x and [opp_pos, x] not in opp_color_positions:
      killed_piece_idx = None
      for idx, piece in enumerate(self.pieces):
        if piece.type == "p" and piece.position == [pos, x]:
          killed_piece_idx = idx
          break

      if killed_piece_idx is not None:
        del self.pieces[killed_piece_idx]

  def _promote_pawn(self, color, piece, upgrade_to="q"):
    """
    Promotes pawn to `updrade_to` type and removes the pawn from the board
    """

    pawn_idx = None
    for idx, _piece in enumerate(self.pieces):
      if _piece.type == piece.type and _piece.position == piece.position:
        pawn_idx = idx
        break

    if pawn_idx is not None:
      del self.pieces[pawn_idx]

    self.pieces.append(Piece(type=upgrade_to, color=piece.color, position=piece.position))

  def _update_position(self, move, is_clone_board=False):
    """
    Updates the piece position, there by updating other pieces' positions based on
    killing/special moves
    Special Moves:
      * Castling
      * En passant
      * Promotion
    """

    for piece in self.pieces:
      if (
        piece.color == move["color"] and
        piece.type == move["piece"] and
        piece.position == move['old_position']
      ):
        piece.position = move['new_position']

        self._kill_piece_if_any(piece)

        if piece.type == "k":
          # if king has moved, then castling privileges are lost on either side
          self.can_castle_king_side = self.can_castle_queen_side = False

          # if king has castled, then update the rook position
          num_blocks_moved = piece.position[1] - move["old_position"][1]
          has_castled = abs(num_blocks_moved) == 2
          is_king_side = num_blocks_moved > 0
          if has_castled:
            self._update_rook_position(self.side_to_move, is_king_side)

        if piece.type == "r":
          # king side castling privilege lost when rook moves from its initial block
          if (self.side_to_move == self.user_color and move['old_position'] == [7, 7]) or (
            self.side_to_move != self.user_color and move['old_position'] == [0, 7]
          ):
            self.can_castle_king_side = False

          # queen side castling privilege lost when rook moves from its initial block
          if (self.side_to_move == self.user_color and move['old_position'] == [7, 0]) or (
            self.side_to_move != self.user_color and move['old_position'] == [0, 0]
          ):
            self.can_castle_queen_side = False

        # promote pawn if it reaches the top of the board
        if piece.type == "p" and piece.position[0] in [0, 7]:
          self._promote_pawn(self.side_to_move, piece)

        last_move = self.moves[-1] if len(self.moves) else None
        if last_move and last_move["piece"].type == "p":
          self._kill_pawn_on_en_passant(last_move, self.side_to_move, move["new_position"])

        self.moves.append({ **move, "piece": piece })

        # print the board, toggle side to move and evaluate if the game is over, when it's NOT a
        # clone board
        if is_clone_board is False:
          str(self)
          self.side_to_move = OPPOSITE[self.side_to_move]
          return self.game_over()

        return
    return

  def play_move(self, move=None):
    if self.side_to_move != self.user_color and move is None:
      move = alpha_beta_pruning(self, self.side_to_move, DEPTH)
    return self._update_position(move)

  def in_check(self, color):
    """
    `color` army is in check if the `color`'s king is in any of the opposite army's moves
    """

    moves = [move['new_position'] for move in self._get_moves(OPPOSITE[color], is_opposition=True)]

    for move in moves:
      for piece in self.pieces:
        if piece.color == color and piece.type == "k" and piece.position in moves:
          return True

    return False

  def in_checkmate(self, color):
    """
    If king is in check and no move can shelter the king, then it's a checkmate!
    """

    if self.in_check(color) is False:
      return False

    for move in self.get_moves(color):
      board = self.clone(move=move)
      if board.in_check(color) is False:
        return False

    return True

  def in_stalemate(self, color):
    """
    If there are no moves for the `color` side and there is no check to it, it's a stalemate!
    """

    moves = self.get_moves(color)
    return len(moves) == 0 and self.in_check(color) is False

  def game_over(self):
    """
    Returns a dictionary containing "who_won" and "by" indicating who won the game and
    by "checkmate" or "stalemate" respectively, when game is over.
    Else, returns None, if there is no checkmate and no stalemate.
    """

    last_move_played_by = OPPOSITE[self.side_to_move]
    if self.in_checkmate(last_move_played_by):
      return { "who_won": last_move_played_by, "by": "checkmate" }

    if self.in_stalemate(last_move_played_by):
      return { "who_won": last_move_played_by, "by": "stalemate" }

    return

  def get_moves(self, color, filter_piece=None, is_opposition=False):
    """
    Returns a list of moves for the `color` side, optionally filtering by `filter_piece` piece type,
    excluding the moves which can cause a check for the `color` side.
    `is_opposition` boolean is enabled when the king's moves are evaluated for castling using the
    opposition color's moves.
    """

    moves = self._get_moves(color, filter_piece=filter_piece, is_opposition=is_opposition)
    return self._exclude_moves_causing_check(color, moves)

  def _get_moves(self, color, filter_piece=None, is_opposition=False):
    pieces = [piece for piece in self.pieces if piece.color == color]
    moves = []

    for piece in pieces:
      if filter_piece is None or (
        piece.type == filter_piece.type and
        piece.position == filter_piece.position and
        piece.color == filter_piece.color
      ):
        legal_moves = PIECE_RULE_METHODS[piece.type]
        moves += [
          {
            "color": color,
            "piece": piece.type,
            "old_position": piece.position,
            "new_position": move
          } for move in legal_moves(self, color, piece.position, is_opposition=is_opposition)
        ]
    return moves

  def _exclude_moves_causing_check(self, color, moves):
    """
    Excludes moves from the list of `moves` which causes check on the board for the `color` side
    """

    if self.in_check(color):
      _moves = []
      for move in moves:
        board = self.clone(move)
        if not board.in_check(color):
          _moves.append(move)

      moves = _moves

    return moves
