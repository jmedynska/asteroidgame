import pygame
import random
from pygame.locals import *
from pygame import Vector2
from pygame.transform import rotozoom
from pygame.mixer import Sound



asteroid_images = ['asteroidgame/images/asteroid1.png', 'asteroidgame/images/asteroid2.png', 'asteroidgame/images/asteroid3.png']

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
            self.forward = self.forward.rotate(-2)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(2)
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
    def __init__(self,position,size):
        self.position = Vector2(position)
        self.size = size
        self.image = pygame.image.load(asteroid_images[size])
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
        
         
def text_positioning(screen,text):
    text_pos = [(screen.get_width() - text.get_width())//2, (screen.get_height()- text.get_height())//2]
    return text_pos

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")
background = pygame.image.load('asteroidgame/images/space.png')
ship = Ship((screen.get_width()//2, screen.get_height()//2))
asteroids = []
out_of_bounds = [-150, -150, 950, 950]
number_of_asteroids = 4

for i in range(number_of_asteroids):
    posx,posy = (random.randint(0, screen.get_width()),
                 random.randint(0, screen.get_height()))
    asteroid_position = (posx,posy)
    asteroid_away_from_screen_center = ((screen.get_width()/2 - posx) * 0.8,
                                         (screen.get_height()/2 - posy) * 0.8)
    asteroid_position += asteroid_away_from_screen_center
    asteroids.append(Asteroid((asteroid_position[0],asteroid_position[1]),0))

game_over = False
font1 = pygame.font.SysFont('Arial', 30, True, False)
font2 = pygame.font.Font('asteroidgame/fonts/Lazer.ttf', 80)
game_over_text = font2.render("Game Over", True, (255,255,255))
win_text = font2.render('You WON!', True, (255,255,255))

clock = pygame.time.Clock()

while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    #images are displayed in the order from bottom to top of the screen
    screen.blit(background,[0,0])  #display the background image on the bottom
    if ship is None:
        screen.blit(game_over_text, text_positioning(screen,game_over_text))
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
        if a.size < 2:
            asteroids.append(Asteroid(a.position, a.size + 1))
            asteroids.append(Asteroid(a.position, a.size + 1))
        asteroids.remove(a)
    if not asteroids:
        screen.blit(win_text, text_positioning(screen,win_text))
    pygame.display.update()

pygame.quit()