# game.py
# This module handles the input & output of the game. Constantly updates the visuals of the board, and recieves the gamestate from chess.py

import pygame # type: ignore
import chess
from common import ROWS, COLS

# Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (100, 200, 100)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Draw each piece at the correct spot
def draw_pieces(pieces):
    for piece in pieces:
        piece_image = pygame.image.load(f"assets\{piece.color}_{piece.type}.png")
        piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(piece_image, (piece.col * SQUARE_SIZE, piece.row * SQUARE_SIZE))

# Draws the chessboard and pieces
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    draw_pieces(chess.pieces)

# Highlights given square
def highlight_square(row, col):
    pygame.draw.rect(screen, HIGHLIGHT,  (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

# Returns the square clicked on (row, col)
def get_square_under_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

highlighted_square = None

# This is the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_square_under_mouse(pos)

            if 0 <= row < ROWS and 0 <= col < COLS:
                chess.board_clicked(row, col)
                if chess.winner:
                     break
                if chess.selected is not None:
                    highlighted_square = (chess.selected.row, chess.selected.col)
                else:
                    highlighted_square = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                chess.u_pressed()
                highlighted_square = None


    draw_board()
    if highlighted_square is not None:
        highlight_square(*highlighted_square)
    pygame.display.flip()
pygame.quit()
