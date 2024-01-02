import pygame


class Node:

    def __init__(self, row, col, width, total_rows):

        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.BLACK = (0, 0, 0)
        self.GREY = (128, 128, 128)
        self.color = self.BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def get_pos(self):
        return self.row, self.col

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].color in [self.BLACK, self.GREY]:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].color in [self.BLACK, self.GREY]:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].color in [self.BLACK, self.GREY]:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].color in [self.BLACK, self.GREY]:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

