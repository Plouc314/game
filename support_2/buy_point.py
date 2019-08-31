import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))

class Background(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Background, self).__init__()
        self.surf = pygame.Surface((800, 600))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

background = Background((255,255,255))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()