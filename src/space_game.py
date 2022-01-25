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
import os
from pygame.constants import *


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_SPEED = 2
FPS = 60

playing = True
# initialize game
pygame.init()

# display a window
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption('Space Command')
clock = pygame.time.Clock()
screen.fill(BLACK)

# get width and height of screen
WIDTH, HEIGHT = pygame.display.get_surface().get_size()

# load images
base_path = os.path.dirname(__file__)
spaceship_path = os.path.join(base_path, 'graphics/spaceship_strong_barrier.png')
spaceShip = pygame.image.load(spaceship_path)
spaceShip = pygame.transform.scale(spaceShip, (250, 410))
game_name_path = os.path.join(base_path, 'graphics/game_logo.png')
game_name = pygame.image.load(game_name_path)
game_name = pygame.transform.scale(game_name, (850, 320))

# load fonts for text
font_path = os.path.join(base_path, 'fonts/Audiowide/Audiowide-Regular.ttf')
game_font = pygame.font.Font(font_path, 35)
text_width, text_height = game_font.size('Press X to start new Game')

# spaceship position
ship_x = (WIDTH * 0.45)
ship_y = (HEIGHT * 0.6)

tmp = 0
move_val = 0


# initialize joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


# display spaceship image
def ship(x, y):
    screen.blit(spaceShip, (x, y))


# mapping our range <-1,1> to <0,1>
def map_range(x):
    y = (x + 1) / 2
    return y


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
        if self.y >= HEIGHT:
            self.y = 0
            self.x = random.randint(1, WIDTH - 1)


class GameScreen:
    def __init__(self):
        self.screen = 'intro'

    def screen_manager(self):
        if self.screen == 'intro':
            self.intro_screen()
        elif self.screen == 'game_screen':
            self.game_play()

    def intro_screen(self) -> None:
        global playing
        screen.blit(game_name, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 450))
        text = game_font.render('Press X to start new Game', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2), HEIGHT - 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
            if event.type == pygame.JOYBUTTONDOWN:
                # print(event, flush=True)
                if event.button == 0:
                    self.screen = 'game_screen'


    def game_play(self) -> None:
        global ship_x, ship_y, playing, tmp, move_val
        # game_status.game_play(ship_x)
        for event in pygame.event.get():

            # trigger buttons ( range -1 to 1)
            if event.type == pygame.JOYAXISMOTION:
                #print(event)
                # left trigger pressed
                if event.axis == 2:
                    if event.value > -1:
                        tmp = event.value
                        move_val = map_range(event.value)
                        # print(tmp, "to", move_val)
                        # move left if button pressed in range
                        if move_val > 0.0 and move_val < 0.7:  # a bit laggy: have to check values again
                            ship_x -= 6
                        # print("moved left")

                # right trigger pressed
                if event.axis == 5:
                    if event.value > -1:
                        tmp = event.value
                        move_val = map_range(event.value)
                        # print(tmp, "to", move_val)
                        # move right if button pressed in range
                        if move_val > 0.0 and move_val < 0.7:  # a bit laggy: have to check values again
                            ship_x += 6
                        # print("moved right")

            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False

        screen.fill(BLACK)

        for star in stars:
            star.draw()
            star.move()
            star.appear_as_new_star()

        ship(ship_x, ship_y)

        pygame.display.update()


stars = []

for i in range(200):
    x_pos = random.randint(1, WIDTH - 1)
    y_pos = random.randint(1, HEIGHT - 1)
    stars.append(Star(x_pos, y_pos, BACKGROUND_SPEED))


game_status = GameScreen()

while playing:
    game_status.screen_manager()
    clock.tick(FPS)

pygame.quit()

# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 
