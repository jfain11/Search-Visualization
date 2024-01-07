import heapq
import random
import time
from queue import PriorityQueue

import pygame
from Node import Node

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (125, 126, 117)
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

    def dijkstra_maze_generation(self, start):
        # Initialize distances and the priority queue
        distances = {node: float('infinity') for row in self.grid for node in row}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            for neighbor in current_node.neighbors:
                new_distance = distances[current_node] + 1

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

        # Mark nodes along the path as walls
        for row in self.grid:
            for node in row:
                if node.color == WHITE and node != start and distances[node] != float('infinity'):
                    node.color = BLACK
                    self.UI.update_screen(self)

    # Usage:
    # Call dijkstra_maze_generation with the starting node to generate a maze using Dijkstra's algorithm.
    # Example: grid.dijkstra_maze_generation(grid.grid[1][1])

    def clear_colors(self):

        for row in range(self.rows):
            for column in range(self.rows):
                node = self.grid[column][row]

                if row == 0 or row == self.rows - 1 or column == 0 or column == self.rows - 1:
                    pass

                elif node.color != BLACK and node.color != WHITE:
                    node.color = WHITE

            time.sleep(0.01)
            self.UI.update_screen(self)

    # ----------------------------------------------------------------------------------------------------------------------

    def draw_nodes(self):

        for row in self.grid:
            for node in row:
                node.draw(self.win)

        # TODO get this to work
        # draw_buttons(win)

    # ----------------------------------------------------------------------------------------------------------------------

    def generate_border(self):
        for i in range(self.rows):
            for j in range(self.rows):
                node = self.grid[i][j]

                # Check if the node is in the border (first or last row or column)
                if i == 0 or i == self.rows - 1 or j == 0 or j == self.rows - 1:
                    node.color = GREY

        # TODO may be an issue
        # update_screen(self.win, self)

    # random mouse ---------------------------------------------------------------------------------------------------------

    def random_mouse_algorithm(self, start, end, color):
        # TODO make it so starting node doesn't turn red.
        # TODO find way to generate a path. maybe run multiple times? multiple rats?
        # TODO if any of the current mouses neighbors are the end then move there.

        mouse = start
        came_from = {}
        counter = 0
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

            counter += 1
            if counter == 5:
                counter = 0
                self.UI.update_screen(self)

    # ------------------------------------------------------------------------------------------------------------------

    def calculate_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def update_grid_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            # SETS PATH
            current.color = PURPLE
            self.UI.update_screen(self)

    def astar_algorithm(self, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[start] = self.calculate_distance(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            # once end node is reached
            if current == end:
                self.reconstruct_path(came_from, end)
                end.color = PURPLE
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.calculate_distance(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        # MAKES OPEN
                        neighbor.color = GREEN

            self.UI.update_screen(self)

            if current != start:
                # MAKES CLOSED
                current.color = RED

        return False

    # ----------------------------------------------------------------------------------------------------------------------
