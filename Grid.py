import random
import time

import pygame
from Node import Node

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

class Grid:

    def __init__(self, size, rows, win, UI):

        self.size = size
        self.rows = rows
        self.grid = []
        self.win = win
        self.UI = UI


    def populate_grid(self):

        gap = self.size // self.rows
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                node = Node(i, j, gap, self.rows)
                self.grid[i].append(node)
        return self.grid

    # ----------------------------------------------------------------------------------------------------------------------

    # TODO may not use
    # def draw_grid(self, win):
    #     gap = WIDTH // ROWS
    #     for i in range(ROWS):
    #         pygame.draw.line(win, GREY, (0, i * gap), (WIDTH, i * gap))
    #         for j in range(ROWS):
    #             pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, WIDTH))

    # ----------------------------------------------------------------------------------------------------------------------

    def generate_obstacles(self):

        for row in range(self.rows):
            for column in range(self.rows):

                node = self.grid[column][row]

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                if row == 0 or row == self.rows - 1 or column == 0 or column == self.rows - 1:
                    pass

                else:
                    if node.color == BLACK:
                        if random.random() < 0.70:
                            node.color = WHITE

                    elif random.random() < 0.30:
                        node.color = BLACK

            time.sleep(0.01)
            self.UI.update_screen(self)



    # ----------------------------------------------------------------------------------------------------------------------

    def draw_nodes(self):

        for row in self.grid:
            for node in row:
                node.draw(self.win)

        # TODO get this to work
        #draw_buttons(win)

    # ----------------------------------------------------------------------------------------------------------------------

    def generate_border(self):
        for i in range(self.rows):
            for j in range(self.rows):
                node = self.grid[i][j]

                # Check if the node is in the border (first or last row or column)
                if i == 0 or i == self.rows - 1 or j == 0 or j == self.rows - 1:
                    node.color = GREY

        # TODO may be an issue
        #update_screen(self.win, self)

    # random mouse ---------------------------------------------------------------------------------------------------------

    def random_mouse_algorithm(self, start, end, color):
        # TODO make it so starting node doesn't turn red.
        # TODO find way to generate a path. maybe run multiple times? multiple rats?
        # TODO if any of the current mouses neighbors are the end then move there.

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

            self.UI.update_screen(self)

    # ----------------------------------------------------------------------------------------------------------------------