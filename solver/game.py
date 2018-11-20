import os

import pygame

WHITE = (255, 255, 255)
GREY = (220, 220, 220)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SIZE = (800, 600)

class UIError(Exception):
    pass

class Button(pygame.sprite.Sprite):

def load_image(name):
    file_path = os.path.join('resources', name)
    try:
       image = pygame.image.load(file_path).convert()
    except pygame.error:
        raise UIError("Could not load image %s" % name)
    return image, image.get_rect()

def main():
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Circuit Solver")
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        w, h = pygame.display.get_surface().get_size()
        screen.fill(GREY)
        pygame.draw.rect(screen, BLACK, (50, h - 70, w - 100, 50), 2)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()