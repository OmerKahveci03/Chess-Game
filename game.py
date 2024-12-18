import pygame
import chess

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
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

# Draws the chessboard. Should draw pieces as well
def draw_board(white_pieces, black_pieces):
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    draw_pieces(white_pieces)
    draw_pieces(black_pieces)

# Highlights given square
def highlight_square(row, col):
    pygame.draw.rect(screen, HIGHLIGHT,  (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

# Returns the square clicked on (row, col)
def get_square_under_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE


white_pieces = []
black_pieces = []
chess.initialize_army(white_pieces, 'white')
chess.initialize_army(black_pieces, 'black')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_square_under_mouse(pos)

            # Check if the click is on the board
            if 0 <= row < ROWS and 0 <= col < COLS:
                print(f"Clicked on board square: ({row}, {col})")  # Log the coordinates
    draw_board(white_pieces, black_pieces)

    pygame.display.flip()

pygame.quit()
