import pygame
import random
from pygame.locals import *
from pygame import Vector2
from pygame.transform import rotozoom
from pygame.mixer import Sound



def wrap_position(position, screen):   # wrapping the movement around the screen
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)

def rotating(position, velocity, image, screen):
    angle = velocity.angle_to(Vector2(0,-1)) #calculating the angle 
    rotated_surface = rotozoom(image, angle, 1.0)   #rotating the image by the angle with scale = 1.0
    rotated_surface_size = Vector2(rotated_surface.get_size())  #getting the size of new rectangle
    blit_position = position - rotated_surface_size // 2
    screen.blit(rotated_surface, blit_position)

class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load('asteroidgame/images/ship.png')
        self.forward = Vector2(0, -2)
        self.bullets = []
        self.can_shoot = 0
        self.drift = (0,0)
        self.shoot_sound = Sound('asteroidgame/sounds/shoot.wav')


    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward/2) / 2
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if is_key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            self.bullets.append(Bullet(Vector2(self.position),self.forward * 5))
            self.shoot_sound.play()
            self.can_shoot = 400
        if self.can_shoot > 0:
            self.can_shoot -= clock.get_time()
        else:
            self.can_shoot = 0
        self.position += self.drift


    def draw(self,screen):
        self.position = wrap_position(self.position, screen)
        rotating(self.position, self.forward, self.image,screen)

class Bullet:
    def __init__(self,position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity

    def draw(self,position):
        pygame.draw.rect(screen,(255,0,0),(self.position.x,self.position.y,5,5))


class Asteroid:
    def __init__(self,position):
        self.position = Vector2(position)
        self.image = pygame.image.load('asteroidgame/images/asteroid1.png')
        self.velocity = Vector2(random.randint(-3,3),random.randint(-3,3))
        self.radius = self.image.get_width() // 2
        self.explode = Sound('./asteroidgame/sounds/explode.mp3')
    
    def update(self):
        self.position += self.velocity


    def draw(self, screen):
        self.position = wrap_position(self.position,screen)
        rotating(self.position, self.velocity, self.image, screen) #display asteroids on the screen

    def hit(self, position):
        if self.position.distance_to(position) <= self.radius:
            self.explode.play()
            return True
        else:
            return False
        
         


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
font = pygame.font.SysFont('Arial', 30, True, False)
game_over_text = font.render("Game Over", True, (255,255,255))
text_pos = [(screen.get_width() - game_over_text.get_width())//2, (screen.get_height()- game_over_text.get_height())//2]

clock = pygame.time.Clock()

while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    #images are displayed in the order from bottom to top of the screen
    screen.blit(background,[0,0])  #display the background image on the bottom
    if ship is None:
        screen.blit(game_over_text,text_pos)
        pygame.display.update()
        continue
    ship.update()
    ship.draw(screen)
    for a in asteroids:
        a.update()
        a.draw(screen)
        if a.hit(ship.position):
            ship = None
            break
    if ship is None:
        continue
    dead_bullets = []
    dead_asteroids = []
    
    for b in ship.bullets:
        b.update()
        b.draw(screen)
        if b.position.x < out_of_bounds[0] or b.position.x > out_of_bounds[2] or \
            b.position.y < out_of_bounds[1] or b.position.y > out_of_bounds[3] and not dead_bullets.__contains__(b):
            dead_bullets.append(b)
        else:
            for a in asteroids:
                if a.hit(b.position):
                    if not dead_bullets.__contains__(b):
                        dead_bullets.append(b)
                    if not dead_asteroids.__contains__(a):
                        dead_asteroids.append(a)
    
    for b in dead_bullets:
        ship.bullets.remove(b)
    for a in dead_asteroids:
        asteroids.remove(a)
    pygame.display.update()

pygame.quit()