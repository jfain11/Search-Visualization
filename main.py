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
    MENU_WIDTH = 400
    HEIGHT = 1200
    ROWS = 100

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

    # ------------------------------------------------------------------------------------------------------------------

    button1_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 60), (300, 100))
    button1 = pygame_gui.elements.UIButton(relative_rect=button1_rect, text='A* Search Algorithm', manager=manager)

    button2_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 190), (300, 100))
    button2 = pygame_gui.elements.UIButton(relative_rect=button2_rect, text='Random Mouse Search Algorithm', manager=manager)

    button3_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 320), (300, 100))
    button3 = pygame_gui.elements.UIButton(relative_rect=button3_rect, text='Click me!', manager=manager)

    button4_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 450), (300, 100))
    button4 = pygame_gui.elements.UIButton(relative_rect=button4_rect, text='Click me!', manager=manager)

    # ------------------------------------------------------------------------------------------------------------------

    # button5_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 100), (300, 100))
    # button5 = pygame_gui.elements.UIButton(relative_rect=button5_rect, text='Click me!', manager=manager)
    #
    # button6_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 100), (300, 100))
    # button6 = pygame_gui.elements.UIButton(relative_rect=button6_rect, text='Click me!', manager=manager)
    #
    # button7_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 100), (300, 100))
    # button7 = pygame_gui.elements.UIButton(relative_rect=button7_rect, text='Click me!', manager=manager)
    #
    # button8_rect = pygame.Rect((GRID_WIDTH + MENU_WIDTH / 10, 100), (300, 100))
    # button8 = pygame_gui.elements.UIButton(relative_rect=button8_rect, text='Click me!', manager=manager)

    # ------------------------------------------------------------------------------------------------------------------

    # main loop --------------------------------------------------------------------------------------------------------

    while running:

        UI.update_screen(grid, pos)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if start and end:

                    # A* SEARCH
                    if event.ui_element == button1:
                        grid.update_grid_neighbors()
                        grid.astar_algorithm(start, end)
                        grid.clear_colors()

                    # Random Mouse Search
                    if event.ui_element == button2:
                        grid.update_grid_neighbors()
                        grid.random_mouse_algorithm(start, end, RED)
                        grid.clear_colors()

                start = None
                end = None

            # LEFT MOUSE CLICK
            if pygame.mouse.get_pressed()[0]:  # LEFT

                try:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    node = grid.grid[row][col]

                    if node.color not in (BLACK, GREY):
                        if not start and node != end:
                            start = node
                            start.color = TURQUOISE

                        elif not end and node != start:
                            end = node
                            end.color = PURPLE
                except:
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.generate_obstacles()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    grid.generate_obstacles()

            manager.process_events(event)

    pygame.quit()

    # ------------------------------------------------------------------------------------------------------------------


main()
