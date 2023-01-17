import pygame
from pygame.locals import *
from pygame import Vector2

class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load('asteroidgame/images/ship.png')

    def update(self):
        pass

    def draw(self,screen):
        screen.blit(self.image, self.position)


pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")
background = pygame.image.load('asteroidgame/images/space.png')
ship = Ship((100,100))
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(background,[0,0])
    ship.update()
    ship.draw(screen)
    pygame.display.update()

pygame.quit()