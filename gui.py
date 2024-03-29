import sys

import pygame

from random import random
from pygame.locals import QUIT

from common.board import Board
from common.constants.pygame import (
  SIZE,
  COLOR_GRAY,
  COLOR_WHITE,
  COLOR_BLUE,
  IMAGE_DIR
)
from common.constants import BLACK, WHITE, OPPOSITE
from common.helpers import get_chess_square, get_chess_square_reverse, get_chess_square_border

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))


def draw_chessboard(board):
  """
  Draws the board with the current `board`'s piece positions
  """

  screen.fill(COLOR_WHITE)

  start_x, start_y = 0, 0
  for idx in range(8):
    if board.user_color == WHITE:
      start_x = 0 if idx % 2 != 0 else SIZE // 8
    else:
      start_x = SIZE // 8 if idx % 2 != 0 else 0

    for __ in range(8):
      pygame.draw.rect(screen, COLOR_GRAY, ((start_x, start_y), (SIZE // 8, SIZE // 8)))
      start_x += 2 * SIZE // 8

    start_y += SIZE // 8

  for piece in board.pieces:
    y, x = piece.position
    img = pygame.image.load(f'{IMAGE_DIR}{piece.color}_{piece.type}.png')
    screen.blit(img, (x * SIZE // 8 + SIZE // 80, y * SIZE // 8 + SIZE // 80))

  pygame.display.update()


def draw_move_borders(board, moves):
  """
  Draws border on square blocks for every move in `moves`
  """

  draw_chessboard(board)

  for move in moves:
    pygame.draw.rect(
      screen,
      COLOR_BLUE,
      (get_chess_square_reverse(SIZE, move[1], move[0]), (SIZE // 8, SIZE // 8))
    )

    if board.user_color != WHITE:
      color = COLOR_WHITE if (move[1] + move[0]) % 2 != 0 else COLOR_GRAY
    else:
      color = COLOR_GRAY if (move[1] + move[0]) % 2 != 0 else COLOR_WHITE

    pygame.draw.rect(
      screen,
      color,
      (get_chess_square_border(SIZE, move[1], move[0]), (SIZE // 8 - 4, SIZE // 8 - 4))
    )

    for piece in board.pieces:
      y, x = piece.position
      if piece.position == move:
        img = pygame.image.load(f'{IMAGE_DIR}{piece.color}_{piece.type}.png')
        screen.blit(img, (x * SIZE // 8 + SIZE // 80, y * SIZE // 8 + SIZE // 80))

  pygame.display.update()


def draw_borders_if_clicked_on_piece(board, x, y):
  """
  Draws borders for moves if clicked on a piece, returning piece clicked on, its moves and its old
  position
  """

  _x, _y = get_chess_square(SIZE, x, y)

  piece_clicked = None
  moves = []
  for piece in board.pieces:
    if piece.position == [_y, _x]:
      moves = [move['new_position'] for move in piece.get_moves(board)]
      piece_clicked = piece.type
      piece_moves = moves

  if moves:
    draw_move_borders(board, moves)

  return (_x, _y), piece_clicked, moves


def looping_cpu_vs_human():
  """
  Player v/s CPU mode
  """
  old_x = 0
  old_y = 0
  new_x = 0
  new_y = 0
  color = WHITE if round(random() * 100) <= 50 else BLACK
  board = Board(color)

  if color != WHITE:
    board.flip()

  draw_chessboard(board)

  if color != WHITE:
    board.play_move()
    draw_chessboard(board)

  piece_clicked = None
  piece_moves = []
  game_over = False
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()
      if not game_over:
        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = pygame.mouse.get_pos()
          old_pos, piece_clicked, piece_moves = draw_borders_if_clicked_on_piece(board, x, y)
          old_x, old_y = old_pos

        if event.type == pygame.MOUSEBUTTONUP:
          x, y = pygame.mouse.get_pos()
          new_x, new_y = get_chess_square(SIZE, x, y)

          if (new_x != old_x or new_y != old_y) and [new_y, new_x] in piece_moves:
            move = {
              "old_position": [old_y, old_x],
              "new_position": [new_y, new_x],
              "piece": piece_clicked,
              "color": board.side_to_move
            }
            is_over = board.play_move(move=move)

            draw_chessboard(board)

            if is_over:
              # TODO: display message
              print(is_over)
              game_over = True
              break
            else:
              is_over = board.play_move()

              draw_chessboard(board)

              if is_over:
                # TODO: display message
                print(is_over)
                game_over = True
                break


def looping_cpu_vs_cpu():
  """
  CPU v/s CPU mode
  """

  board = Board()
  draw_chessboard(board)

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()

    is_over = board.play_move()
    draw_chessboard(board)

    if is_over:
      # TODO: display message
      break


def looping_human_vs_human():
  """
  Human v/s Human mode
  """

  old_x = 0
  old_y = 0
  new_x = 0
  new_y = 0
  board = Board()

  draw_chessboard(board)

  piece_clicked = None
  piece_moves = []
  game_over = False
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
        pygame.display.update()
      if not game_over:
        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = pygame.mouse.get_pos()
          piece_moves = draw_borders_if_clicked_on_piece(board, x, y)

        if event.type == pygame.MOUSEBUTTONUP:
          x, y = pygame.mouse.get_pos()
          new_x, new_y = get_chess_square(SIZE, x, y)
          if (new_x != old_x or new_y != old_y) and [new_y, new_x] in piece_moves:
            move = {
              "old_position": [old_y, old_x],
              "new_position": [new_y, new_x],
              "piece": piece_clicked,
              "color": board.side_to_move
            }

            is_over = board.play_move(move=move)
            if is_over:
              # TODO: display message
              print(is_over)
              game_over = True
              break

            board.user_color = OPPOSITE[board.user_color]
            board.flip()

            draw_chessboard(board)
