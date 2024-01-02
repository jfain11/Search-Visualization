import random
from Node import Node
import pygame
import math
from queue import PriorityQueue
import pygame_gui

# TODO fix issue with rows > 50 not correctly generating borders

GRID_WIDTH = 800
HEIGHT = 800
MENU_WIDTH = 400
ROWS = 50

WIN = pygame.display.set_mode((GRID_WIDTH + MENU_WIDTH, HEIGHT), pygame.NOFRAME)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# ----------------------------------------------------------------------------------------------------------------------

def populate_grid():

    grid = []
    gap = GRID_WIDTH // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j, gap, ROWS)
            grid[i].append(node)
    return grid

# ----------------------------------------------------------------------------------------------------------------------

def draw_grid(win):
    gap = GRID_WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * gap), (GRID_WIDTH, i * gap))
        for j in range(ROWS):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, GRID_WIDTH))

# ----------------------------------------------------------------------------------------------------------------------

def update_screen(win, grid):
    win.fill(BLACK)

    for row in grid:
        for spot in row:

            spot.draw(win)

        draw_buttons(win)

    #draw_grid(win, ROWS, width)
    pygame.display.update()

# ----------------------------------------------------------------------------------------------------------------------

def generate_obstacles(win, grid):

    for row in range(ROWS):
        for column in range(ROWS):

            node = grid[column][row]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if row == 0 or row == ROWS - 1 or column == 0 or column == ROWS - 1:
                pass

            else:
                if node.color == BLACK:
                    if random.random() < 0.70:
                        node.color = WHITE

                elif random.random() < 0.30:
                    node.color = BLACK

        update_screen(win, grid)

# ----------------------------------------------------------------------------------------------------------------------

def generate_border(win, grid):
    for i in range(ROWS):
        for j in range(ROWS):
            node = grid[i][j]

            # Check if the node is in the border (first or last row or column)
            if i == 0 or i == ROWS - 1 or j == 0 or j == ROWS - 1:
                node.color = GREY


    update_screen(win, grid)

# ----------------------------------------------------------------------------------------------------------------------

def draw_buttons(win):

    # TODO draw buttons using image successfully
    # TODO create button class
    # TODO methods to know when clicked and to change when clicked/hovered over

    b1_rect = pygame.Rect(GRID_WIDTH + 40, 50, MENU_WIDTH - 100, 40)
    b1_img = pygame.image.load('button_random-mouse-algorithm.png')


    # button2 = pygame.draw.rect(win, RED, (WIDTH + 40, 120, GRID_WIDTH - 100, 40))
    # button3 = pygame.draw.rect(win, RED, (WIDTH + 40, 190, GRID_WIDTH - 100, 40))


    # button_image1 = pygame.transform.scale(rm_button, (button1.width, button1.height))
    # pygame.draw.rect(win, button_image1)

    # border
    # TOP BORDER
    pygame.draw.rect(win, GREY, (GRID_WIDTH, 0, MENU_WIDTH, GRID_WIDTH / ROWS))
    # BOTTOM BORDER
    pygame.draw.rect(win, GREY, (GRID_WIDTH, GRID_WIDTH - (GRID_WIDTH / ROWS), MENU_WIDTH, GRID_WIDTH / ROWS))
    # RIGHT BORDER
    pygame.draw.rect(win, GREY, (GRID_WIDTH + MENU_WIDTH - (GRID_WIDTH / ROWS), 0, GRID_WIDTH / ROWS, GRID_WIDTH))

# A* -------------------------------------------------------------------------------------------------------------------

def h(p1, p2):
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
    f_score[start] = h(start.get_pos(), end.get_pos())

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
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
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

# random mouse ---------------------------------------------------------------------------------------------------------

def random_mouse_algorithm(update, grid, start, end, color):

    # TODO make it so starting node doesn't turn red.
    # TODO find way to generate a path. maybe run multiple times? multiple rats?

    mouse = start
    came_from = {}

    while mouse != end:

        mouse.color = color

        # Create a list of neighbors to be removed
        neighbors_to_remove = [neighbor for neighbor in mouse.neighbors if neighbor.color == color]

        # Remove neighbors with the color RED
        for neighbor in neighbors_to_remove:
            mouse.neighbors.remove(neighbor)

        if len(mouse.neighbors) > 0:
            next_node = random.choice(mouse.neighbors)
            came_from[next_node] = mouse
            mouse = next_node

        else:
            mouse = came_from[mouse]

        update()

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

    # TODO look into abstracting code into classes.


    grid = populate_grid()
    generate_border(WIN, grid)

    running = True
    obstacles_generated = False
    start = None
    end = None

    while running:

        update_screen(WIN, grid)

        # generates obstacles
        if not obstacles_generated:
            generate_obstacles(WIN, grid)
            obstacles_generated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.color = TURQUOISE

                elif not end and node != start:
                    end = node
                    end.color = PURPLE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_obstacles(WIN, grid)

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and start and end:
            #         for row in grid:
            #             for node in row:
            #                 node.update_neighbors(grid)
            #
            #         #astar_algorithm(lambda: update_screen(win, grid), grid, start, end)
            #         random_mouse_algorithm(lambda: update_screen(win, grid), grid, start, end, YELLOW)




    pygame.quit()




main()