
import pygame
from queue import PriorityQueue

from User_Interface import User_Interface
from Grid import Grid

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (125, 126, 1117)
TURQUOISE = (64, 224, 208)



# ----------------------------------------------------------------------------------------------------------------------

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# ----------------------------------------------------------------------------------------------------------------------

def main():

    # TODO algorithm ideas:
    #       ant colony optimization - used to find paths or generate maze
    #       wall hugger - need actual maze
    #       dead end filler - need actual maze

    # TODO different obstacle generation. I would like to generate an actual maze.

    # TODO fix issue with rows > 50 not correctly generating borders

    GRID_WIDTH = 800
    MENU_WIDTH = 400
    HEIGHT = 800
    ROWS = 50

    win = pygame.display.set_mode((GRID_WIDTH + MENU_WIDTH, HEIGHT), pygame.NOFRAME)
    UI = User_Interface(win, ROWS, GRID_WIDTH, MENU_WIDTH)
    grid = Grid(GRID_WIDTH, ROWS, win, UI)

    running = True
    start = None
    end = None

    grid.populate_grid()
    grid.generate_border()
    grid.generate_obstacles()
    pos = pygame.mouse.get_pos()


    # main loop --------------------------------------------------------------------------------------------------------
    while running:


        UI.update_screen(grid, pos)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




            # TODO if click is outside of grid dont crash
            if pygame.mouse.get_pressed()[0]:  # LEFT
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                node = grid.grid[row][col]
                if not start and node != end:
                    start = node
                    start.color = TURQUOISE

                elif not end and node != start:
                    end = node
                    end.color = PURPLE

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         grid.generate_obstacles()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid.grid:
                        for node in row:
                            node.update_neighbors(grid.grid)

                    #grid.astar_algorithm(start, end)
                    grid.random_mouse_algorithm(start, end, YELLOW)

    pygame.quit()

    # ------------------------------------------------------------------------------------------------------------------

main()