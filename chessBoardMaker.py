import pygame
import random
import sys

def load_tile(surface, row, col, tile_size=192, x_gap=26, y_gap=30):
    # Calculate the position of the tile in the sprite sheet
    x = col * (tile_size + x_gap)
    y = row * (tile_size + y_gap)
    tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    tile.blit(surface, (0, 0), (x, y, tile_size, tile_size))
    return tile

def main():
    pygame.init()

    # Board dimensions
    board_width = 5
    board_height = 3

    # Original tile size before scaling
    tile_size = 192
    x_gap = 26
    y_gap = 30

    # We will scale tiles down to 1/4 their size
    scale_factor = 1/2
    scaled_tile_size = int(tile_size * scale_factor)

    # Gap between squares (no gap after last column/row)
    gap = 10

    # Outer margin around the entire board
    outer_margin = 30

    # Probability of selecting a top-row (plain) tile vs enhanced
    top_row_probability = 0.7

    # Background image path
    background_path = "grass.jpg"  # Replace with your actual background image file

    # Calculate the screen size
    # Total width = margin*2 + board_width*tile_size + (board_width-1)*gap
    screen_width = outer_margin * 2 + board_width * scaled_tile_size + (board_width - 1) * gap
    screen_height = outer_margin * 2 + board_height * scaled_tile_size + (board_height - 1) * gap

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
    pygame.display.set_caption("Random Scaled Chess Board")

    # Load the sprite sheet after the display is initialized
    sprite_sheet = pygame.image.load("squares1.png").convert_alpha()

    # Preload all tiles and scale them down
    tiles = [[load_tile(sprite_sheet, r, c, tile_size, x_gap, y_gap) for c in range(6)] for r in range(6)]
    for r in range(6):
        for c in range(6):
            tiles[r][c] = pygame.transform.smoothscale(tiles[r][c], (scaled_tile_size, scaled_tile_size))

    # Load and scale the background image
    background_image = pygame.image.load(background_path).convert()
    background_image = pygame.transform.smoothscale(background_image, (screen_width, screen_height))

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw the board on top of the background
    # White squares on (x+y) even; black squares on (x+y) odd
    # White tiles columns: 0,1,2; Black tiles columns: 3,4,5
    # Plain row: 0; Enhanced rows: 1-5

    for y in range(board_height):
        for x in range(board_width):
            is_white = ((x + y) % 2 == 0)

            # Decide tile row
            if random.random() < top_row_probability:
                tile_row = 0
            else:
                tile_row = random.randint(1, 5)

            # Decide tile column based on color
            if is_white:
                tile_col = random.randint(0, 2)
            else:
                tile_col = random.randint(3, 5)

            chosen_tile = tiles[tile_row][tile_col]

            # Calculate position including outer margin and gaps
            draw_x = outer_margin + x * (scaled_tile_size + gap)
            draw_y = outer_margin + y * (scaled_tile_size + gap)

            screen.blit(chosen_tile, (draw_x, draw_y))

    pygame.display.flip()

    # Event loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
