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

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYING = True
BACKGROUND_SPEED = 5


# initialize game
pygame.init()

# display a window
screen = pygame.display.set_mode((0, 0))
screen.fill(BLACK)

while PLAYING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            PLAYING = False
            pygame.quit()
