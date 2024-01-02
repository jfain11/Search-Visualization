
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
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# ----------------------------------------------------------------------------------------------------------------------

def calculate_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        # SETS PATH
        current.color = PURPLE
        draw()

def astar_algorithm(update, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = calculate_distance(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        # once end node is reached
        if current == end:
            reconstruct_path(came_from, end, update)
            end.color = PURPLE
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + calculate_distance(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    # MAKES OPEN
                    neighbor.color = GREEN

        update()

        if current != start:
            # MAKES CLOSED
            current.color = RED

    return False

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

    # main loop --------------------------------------------------------------------------------------------------------
    while running:

        UI.update_screen(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
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

                    #astar_algorithm(lambda: update_screen(win, grid), grid, start, end)
                    grid.random_mouse_algorithm(start, end, YELLOW)

    pygame.quit()

    # ------------------------------------------------------------------------------------------------------------------

main()