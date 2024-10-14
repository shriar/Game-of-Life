import pygame
import numpy as np
import time

pygame.init()

# Set up the display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Grid")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (220, 220, 220)
RED = (255, 0, 0)

# Grid settings
cell_size = 5
rows = height // cell_size
cols = width // cell_size
print(f"Grid: {rows} * {cols}")

grid_value = np.zeros((rows, cols))
# Gosper glider gun pattern
# gun_pattern = [
#     (1, 5), (1, 6), (2, 5), (2, 6),  # Left block
#     (11, 5), (11, 6), (11, 7), (12, 4), (12, 8), (13, 3), (13, 9),
#     (14, 3), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5), (17, 6), (17, 7),
#     (18, 6),  # Right side of gun
#     (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6),
#     (25, 1), (25, 2), (25, 6), (25, 7),  # Right block
#     (35, 3), (35, 4), (36, 3), (36, 4)  # Far right block
# ]
# for x, y in gun_pattern:
#     if x < rows and y < cols:
#         grid_value[y+10, x+10] = 1


# Create a block-and-stick pattern that will grow infinitely
pattern = [
    (0, 1), (1, 0), (1, 1), (1, 2), (2, 2)
]

# Calculate the center of the grid
center_row = rows // 2
center_col = cols // 2

# Place the pattern near the center of the grid
for row, col in pattern:
    grid_row = (center_row - 2 + row) % rows
    grid_col = (center_col - 2 + col) % cols
    grid_value[grid_row, grid_col] = 1


def no_of_neighbors(grid_value, row, col):
    count = 0
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i >= 0 and j >= 0 and i < rows and j < cols:
                count += grid_value[i, j]
    count -= grid_value[row, col]
    return count

generation = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE) # Fill the screen with white

    new_grid = np.copy(grid_value)

    for row in range(rows):
        for col in range(cols):
            loc_x = col * cell_size
            loc_y = row * cell_size
            no_neightbour = no_of_neighbors(grid_value, row, col)

            pygame.draw.rect(screen, BLACK, (loc_x, loc_y, cell_size, cell_size), 1) # draw  grid

            if grid_value[row, col] == 1:
                pygame.draw.rect(screen, RED, (loc_x, loc_y, cell_size, cell_size), 0)
                pygame.draw.rect(screen, BLACK, (loc_x, loc_y, cell_size, cell_size), 1)
            
            # Apply Conway's Game of Life rules
            if grid_value[row, col] == 1:  # Cell is alive
                if no_neightbour < 2 or no_neightbour > 3:
                    new_grid[row, col] = 0  # Cell dies
            else:  # Cell is dead
                if no_neightbour == 3:
                    new_grid[row, col] = 1  # Cell becomes alive

    grid_value = new_grid

    population = np.sum(grid_value)
    
    # Render text for population and generation
    font = pygame.font.Font(None, 24)
    population_text = font.render(f"Population: {population}", True, (0, 0, 255))
    generation_text = font.render(f"Generation: {generation}", True, (0, 0, 255))
    
    # Display text on screen
    screen.blit(population_text, (10, 10))
    screen.blit(generation_text, (10, 30))
    
    generation += 1


    clock.tick(60)
    pygame.time.wait(10)
    pygame.display.flip()

pygame.quit()
