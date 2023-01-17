import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.fill((0,0,0))
    pygame.display.update()

pygame.quit()