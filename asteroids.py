import pygame
from pygame.locals import *
from pygame import Vector2
from pygame.transform import rotozoom
import random

class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load('asteroidgame/images/ship.png')
        self.forward = Vector2(0, -1)


    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)


    def draw(self,screen):
        angle = self.forward.angle_to(Vector2(0,-1)) #calculating the angle 
        rotated_surface = rotozoom(self.image, angle, 1.0)   #rotating the image by the angle with scale = 1.0
        rotated_surface_size = Vector2(rotated_surface.get_size())  #getting the size of new rectangle
        blit_position = self.position - rotated_surface_size // 2
        screen.blit(rotated_surface, blit_position)


class Asteroid:
    def __init__(self,position):
        self.position = Vector2(position)
        self.image = pygame.image.load('asteroidgame/images/asteroid1.png')
        self.velocity = Vector2(random.randint(-3,3),random.randint(-3,3))
    
    def update(self):
        self.position += self.velocity
        if self.position.x < out_of_bounds[0] or self.position.x > out_of_bounds[2]:
            self.velocity.x *= -1
            self.velocity.y = random.randint(-3,3)
        if self.position.y < out_of_bounds[1] or self.position.y > out_of_bounds[3]:
            self.velocity.y *= -1
            self.velocity.x = random.randint(-3,3)

    def draw(self, position):
         screen.blit(self.image, self.position)   #display asteroids on the screen


pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")
background = pygame.image.load('asteroidgame/images/space.png')
ship = Ship((100,700))
asteroids = []
out_of_bounds = [-150, -150, 950, 950]
for i in range(10):
    asteroids.append(Asteroid((random.randint(0, screen.get_width()),random.randint(0, screen.get_height()))))
game_over = False
clock = pygame.time.Clock()

while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    #images are displayed in the order from bottom to top of the screen
    screen.blit(background,[0,0])  #display the background image on the bottom
    ship.update()
    ship.draw(screen)
    for a in asteroids:
        a.update()
        a.draw(screen)

    pygame.display.update()

pygame.quit()