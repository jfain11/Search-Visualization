
import pygame
from queue import PriorityQueue
import pygame_gui
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

    pygame.init()

    GRID_WIDTH = 1200
    MENU_WIDTH = 800
    HEIGHT = 1200
    ROWS = 50

    win = pygame.display.set_mode((GRID_WIDTH + MENU_WIDTH, HEIGHT), pygame.NOFRAME)
    manager = pygame_gui.UIManager((GRID_WIDTH + MENU_WIDTH, HEIGHT))
    UI = User_Interface(win, manager, ROWS, GRID_WIDTH, MENU_WIDTH)
    grid = Grid(GRID_WIDTH, ROWS, win, UI)


    running = True
    start = None
    end = None

    grid.populate_grid()
    grid.generate_border()
    grid.generate_obstacles()
    pos = pygame.mouse.get_pos()

    button_rect = pygame.Rect((850, 100), (200, 50))
    button = pygame_gui.elements.UIButton(relative_rect=button_rect, text='Click me!', manager=manager)

    # Create another button
    another_button_rect = pygame.Rect((850, 200), (200, 50))
    another_button = pygame_gui.elements.UIButton(relative_rect=another_button_rect, text='Another Button',
                                                  manager=manager)


    # main loop --------------------------------------------------------------------------------------------------------

    while running:

        UI.update_screen(grid, pos)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button:
                        grid.generate_obstacles()


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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.generate_obstacles()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and start and end:
            #         for row in grid.grid:
            #             for node in row:
            #                 node.update_neighbors(grid.grid)
            #
            #         #grid.astar_algorithm(start, end)
            #         #grid.random_mouse_algorithm(start, end, YELLOW)


    pygame.quit()

    # ------------------------------------------------------------------------------------------------------------------

main()