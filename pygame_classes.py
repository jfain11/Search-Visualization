import pygame


class Button:
    def __init__(self, win, x, y, width, height, idle_img_path, hover_image_path, pressed_img_path):

        self.win = win

        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)

        self.idle_img, self.hover_img, self.pressed_img = self._load_images(
            idle_img_path, hover_image_path, pressed_img_path)

        self.is_hovered = False
        self.is_pressed = False


    def _load_images(self, idle_img_path, hover_img_path, pressed_img_path):

        idle_img = pygame.image.load(idle_img_path)
        hover_img = pygame.image.load(hover_img_path)
        pressed_img = pygame.image.load(pressed_img_path)

        idle_img = pygame.transform.scale(idle_img, (self.width, self.height))
        hover_img = pygame.transform.scale(hover_img, (self.width, self.height))
        pressed_img = pygame.transform.scale(pressed_img, (self.width, self.height))

        return idle_img, hover_img, pressed_img


    def draw(self, style):

        if style == 'pressed':
            self.win.blit(self.pressed_img, self.rect)
        elif style == "hover":
            self.win.blit(self.hover_img, self.rect)
        elif style == 'idle':
            self.win.blit(self.idle_img, self.rect)

    def check_hover(self, pos):
        return self.rect.collidepoint(pos)


