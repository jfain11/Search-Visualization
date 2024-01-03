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
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class User_Interface:

    def __init__(self, win, rows, grid_width, menu_width):

        self.win = win
        self.grid_width = grid_width
        self.menu_width = menu_width
        self.rows = rows
        self.buttons = []

    def update_screen(self, grid, pos=None):

        self.win.fill(BLACK)
        grid.draw_nodes()
        self.draw_buttons(pos)
        self.draw_menu_border()
        # optional: draw grid lines here
        pygame.display.update()

    def create_buttons(self):
        pass

    def draw_buttons(self, pos):
        # TODO draw buttons using image successfully
        # TODO create button class
        # TODO methods to know when clicked and to change when clicked/hovered over

        # b1_rect = pygame.Rect(grid_width + 40, 50, GRID_WIDTH - 100, 40)
        # b1_img = pygame.image.load('button_random-mouse-algorithm.png')

        b1 = Button(self.win, self.grid_width + 20, 120, 160, 50,
                    'mouse_idle.png',
                    'mouse_hover.png',
                    'mouse_pressed.png')

        self.buttons.append(b1)

        if pos:
            for button in self.buttons:
                if button.check_hover(pos):
                    b1.draw('hover')
                else:
                    b1.draw('idle')


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

        # RIGHT BORDER
        pygame.draw.rect(self.win, GREY, (
            self.grid_width + self.menu_width - (self.grid_width / self.rows),
            0,
            self.grid_width / self.rows,
            self.grid_width))

    # ------------------------------------------------------------------------------------------------------------------
