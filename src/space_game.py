#!/usr/bin/env/python3

"""
------------------------------------------------------------------------------------------------
 @authors       Nicola Lea Libera (117073), Laura Simon (), Chiranjeevi Janjanam()
------------------------------------------------------------------------------------------------
 Description: This is the implementation of a little space game that detects if a player is
              pressing the buttons too hard and punishes him/her if this is the case.
              The goal of the game is to help train people to stay calm even in stressful
              situations.
------------------------------------------------------------------------------------------------
"""

import pygame
import random
temp = 0
moveVal = 0

from pygame.constants import JOYAXISMOTION

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYING = True
BACKGROUND_SPEED = 2
FPS = 60


# initialize game
pygame.init()

# display a window
screen = pygame.display.set_mode((0, 0))
clock = pygame.time.Clock()
screen.fill(BLACK)

#load images
#path have to be adapted depending where image is at each
spaceShip = pygame.image.load('.\src\graphics\spaceCow.png')

# initialize joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# logic for moving stars in background
width, height = pygame.display.get_surface().get_size()


class Star(object):
    def __init__(self, x, y, speed):
        self.radius = 1
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.speed

    def appear_as_new_star(self):
        if self.y >= height:
            self.y = 0
            self.x = random.randint(1, width - 1)


stars = []

for i in range(200):
    x_pos = random.randint(1, width - 1)
    y_pos = random.randint(1, height - 1)
    stars.append(Star(x_pos, y_pos, BACKGROUND_SPEED))


# spaceship position 
ship_x = (width * 0.45)
ship_y = (height * 0.6)

#display spaceship image
def ship(x,y):
    screen.blit(spaceShip, (x,y))



#mapping our range <-1,1> to <0,1>
def maprange(x):
    y = (x+1) / 2
    return y
    

while PLAYING:
    for event in pygame.event.get():

        #trigger buttons ( range -1 to 1)
        if event.type == JOYAXISMOTION:
            #print(event)

            #left trigger pressed
            if event.axis == 4:
                if event.value > -1:
                   temp = event.value
                   moveVal = maprange(event.value)
                   #print(temp, "to", moveVal)
                   #move left if button pressed
                   ship_x -= 4
                   #print("moved left")
                   

            #right trigger pressed
            if event.axis == 5:
                if event.value > -1:
                   temp = event.value
                   moveVal = maprange(event.value)
                   #print(temp, "to", moveVal)
                   #move right if button pressed
                   ship_x += 4
                   #print("moved right")

            # to do: find right movement range 
            #        fix double movement through multiple values
            #        use range/mapping for bug/evaluation   
            

        if event.type == pygame.QUIT:
            PLAYING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            PLAYING = False

    screen.fill(BLACK)

    for star in stars:
        star.draw()
        star.move()
        star.appear_as_new_star()

    ship(ship_x,ship_y)

    pygame.display.flip()
    clock.tick(FPS)

    
    

pygame.quit()

# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 