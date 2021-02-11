def get_chess_square(size, x, y):
  return [ x // (size // 8), y // (size // 8) ]


def get_chess_square_reverse(size, a, b):
  return (a * size // 8, b * size // 8)  


def get_chess_square_border(size, r, s):
  return (r * size // 8 + 2, s * size // 8 + 2)
