import pygame
from pygame_classes import Button


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (125, 126, 117)
TURQUOISE = (64, 224, 208)

class User_Interface:

    def __init__(self, win, manager, rows, grid_width, menu_width):

        self.win = win
        self.manager = manager
        self.grid_width = grid_width
        self.menu_width = menu_width
        self.rows = rows
        self.buttons = []

    def update_screen(self, grid, pos=None):

        self.win.fill(BLACK)
        grid.draw_nodes()
        self.draw_menu_border()
        # optional: draw grid lines here

        self.manager.update(30)
        self.manager.draw_ui(self.win)

        pygame.display.update()


    def draw_menu_border(self):

        # TOP BORDER
        pygame.draw.rect(self.win, GREY, (
            self.grid_width,
            0,
            self.menu_width,
            self.grid_width / self.rows))

        # BOTTOM BORDER
        pygame.draw.rect(self.win, GREY, (
            self.grid_width,
            self.grid_width - (self.grid_width / self.rows),
            self.menu_width,
            self.grid_width / self.rows))

        # MIDDLE BORDER
        pygame.draw.rect(self.win, GREY, (
            self.grid_width,
            self.grid_width / 2 - 10,
            self.menu_width,
            self.grid_width / self.rows))

        # RIGHT BORDER
        pygame.draw.rect(self.win, GREY, (
            self.grid_width + self.menu_width - (self.grid_width / self.rows),
            0,
            self.grid_width / self.rows,
            self.grid_width))

    # ------------------------------------------------------------------------------------------------------------------
