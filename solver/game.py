import os

import pygame

# Constants
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
D_GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SIZE = (800, 600)
RESISTOR = 'resistor.png'
VS = 'voltage source.png'
CS = 'current source.png'


class UIError(Exception):
    pass


class Button(pygame.sprite.Sprite):

    def __init__(self, image, location=None, scale=12):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, scale=scale)
        self.image.set_colorkey(BLACK)
        if location is not None:
            self.rect.x, self.rect.y = location

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, D_GREY, self.rect)
            self.draw(screen)


def load_image(name, scale=12):
    folder = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(folder, 'resources', name)
    try:
        image = pygame.image.load(file_path).convert_alpha()
    except pygame.error:
        raise UIError("Could not load image %s" % name)
    image = pygame.transform.smoothscale(image, [i // scale for i in
                                                 image.get_size()])
    return image, image.get_rect()


def main():
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Circuit Solver")
    running = True
    r = Button(RESISTOR, scale=10, location=(200, 200))
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        w, h = pygame.display.get_surface().get_size()
        screen.fill(GREY)
        r.draw(screen)
        r.update(screen)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()