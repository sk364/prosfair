def get_chess_square(size, x, y):
  """
  Returns the coordinates of the square block given mouse position `x` and `y`
  """

  return (x // (size // 8), y // (size // 8))


def get_chess_square_reverse(size, x, y):
  """
  Returns the coordinates of the start of the square block on the board given the block's
  coordinates
  """

  return (x * size // 8, y * size // 8)


def get_chess_square_border(size, x, y):
  """
  Returns the coordinates of the square block's border
  """

  return (x * size // 8 + 2, y * size // 8 + 2)
