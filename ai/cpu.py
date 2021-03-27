from common.constants import OPPOSITE


def get_pawn_counts(board, color):
  """
  computes number of doubled, isolated, blocked and connected pawns for a side
  """

  own_army_positions = [piece.position for piece in board.pieces if piece.color == color]
  opposite_army_positions = [piece.position for piece in board.pieces if piece.color != color]

  own_pawn_positions = [
    piece.position for piece in board.pieces if piece.color == color and piece.type == 'p']
  opposite_pawn_positions = [
    piece.position for piece in board.pieces if piece.color != color and piece.type == 'p']

  pawn_counts = {
    "doubled": 0,
    "blocked": 0,
    "isolated": 0,
    "connected": 0
  }
  pawns = [piece for piece in board.pieces if piece.color == color and piece.type == 'p']
  for pawn in pawns:
    y, x = pawn.position

    one_step_ahead = y + 1 if board.user_color != color else y - 1
    if [one_step_ahead, x] in opposite_army_positions:
      if (
        [one_step_ahead, x + 1] not in opposite_army_positions and
        [one_step_ahead, x - 1] not in opposite_army_positions
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


def compute_piece_value(board, color):
  sum_of_pieces = 0
  for piece in [p for p in board.pieces if p.color == color]:
    sum_of_pieces += piece.get_value(color)
  return sum_of_pieces


def compute_mobility(board, color):
  """
  returns number of valid positions for a side
  """
  return len(board.get_moves(color))


def evaluate_board(board):
  """
  evaluates the board using
   - piece values
   - piece square tables
   - pawn structure
   - mobility of pieces
  """
  color = OPPOSITE[board.user_color]
  if board.in_checkmate(color):
    return float('-inf')
  if board.in_checkmate(OPPOSITE[color]):
    return float('inf')

  sum_of_pieces_1 = compute_piece_value(board, color)
  sum_of_pieces_2 = compute_piece_value(board, OPPOSITE[color])
  pawn_counts_1 = get_pawn_counts(board, color)
  pawn_counts_2 = get_pawn_counts(board, OPPOSITE[color])
  mobility_1 = compute_mobility(board, color)
  mobility_2 = compute_mobility(board, OPPOSITE[color])

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
