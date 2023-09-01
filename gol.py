import pygame
import numpy as np
import random

CELL_SIZE = 5
WIDTH, HEIGHT = 650, 650
BACKGROUND_COLOR = (0, 0, 0)
NEW_CELL_COLOR = (0, 0, 255)
CELL_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

grid_shape = ((WIDTH - CELL_SIZE) // CELL_SIZE, (HEIGHT - CELL_SIZE) // CELL_SIZE)
grid = np.zeros((2, *grid_shape), dtype=int)

# Main loop
start = False
mouse_pressed = False
cycle_count = 0
while True:
    # Drawing
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            x, y = event.pos
            if not start and x < WIDTH - CELL_SIZE and y < HEIGHT - CELL_SIZE:
                grid[0, x // CELL_SIZE, y // CELL_SIZE] = not grid[0, x // CELL_SIZE, y // CELL_SIZE]
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if not start and mouse_pressed and x < WIDTH - CELL_SIZE and y < HEIGHT - CELL_SIZE:
                grid[0, x // CELL_SIZE, y // CELL_SIZE] = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = not start

    # Grid drawing
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            if grid[0, i, j]:
                color = CELL_COLOR if grid[1, i, j] else NEW_CELL_COLOR
                pygame.draw.rect(screen, color, pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

    # Grid update
    if start:
        cycle_count += 1
        if cycle_count % 10 == 0:  
            random_cell = (random.randint(0, grid_shape[0] - 1), random.randint(0, grid_shape[1] - 1))
            while grid[0, random_cell[0], random_cell[1]] == 1:
                random_cell = (random.randint(0, grid_shape[0] - 1), random.randint(0, grid_shape[1] - 1))
            grid[0, random_cell[0], random_cell[1]] = 1

        new_grid = grid.copy()
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                total = (grid[0, i, (j - 1) % grid_shape[1]] + grid[0, i, (j + 1) % grid_shape[1]] +
                         grid[0, (i - 1) % grid_shape[0], j] + grid[0, (i + 1) % grid_shape[0], j] +
                         grid[0, (i - 1) % grid_shape[0], (j - 1) % grid_shape[1]] + grid[0, (i - 1) % grid_shape[0], (j + 1) % grid_shape[1]] +
                         grid[0, (i + 1) % grid_shape[0], (j - 1) % grid_shape[1]] + grid[0, (i + 1) % grid_shape[0], (j + 1) % grid_shape[1]])
                if grid[0, i, j]:
                    if total < 2 or total > 3:
                        new_grid[0, i, j] = 0
                elif total == 3:
                    new_grid[0, i, j] = 1
        grid[1] = grid[0]
        grid[0] = new_grid[0]