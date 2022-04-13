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
import numpy as np
import matplotlib.pyplot as plt

from pygame.constants import *


# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEW_OPPONENT = ['asteroid', 'cow']
OPPONENT_WEIGHTS = [9, 1]
BACKGROUND_SPEED = 5
FPS = 60
NUM_OF_LEVELS = 5

playing = True
# initialize game
pygame.init()

# display a window
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Space Command')
clock = pygame.time.Clock()
screen.fill(BLACK)

# get width and height of screen
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
tmp = 0
move_val = 0
velocity = 0
contr = 4
game_speed = 5.5
level = 1
score = 0
colorBord = (131, 139, 139)
color_tmp = (124, 252, 0)
height = 0

# load images
base_path = os.path.dirname(__file__)
# spaceship with blue flames indicating full speed mode
spaceship_strong_barrier_path = os.path.join(base_path, 'graphics/spaceship_strong_barrier.png')
spaceship_strong_barrier_image = pygame.image.load(spaceship_strong_barrier_path)
spaceship_strong_barrier_image = pygame.transform.scale(spaceship_strong_barrier_image, (140, 260))

spaceship_weak_barrier_path = os.path.join(base_path, 'graphics/spaceship_weak_barrier.png')
spaceship_weak_barrier_image = pygame.image.load(spaceship_weak_barrier_path)
spaceship_weak_barrier_image = pygame.transform.scale(spaceship_weak_barrier_image, (140, 260))

spaceship_no_barrier_path = os.path.join(base_path, 'graphics/spaceship_no_barrier.png')
spaceship_no_barrier_image = pygame.image.load(spaceship_no_barrier_path)
spaceship_no_barrier_image = pygame.transform.scale(spaceship_no_barrier_image, (140, 260))

# spaceship with red flames indicating lower speed mode
spaceship_red_strong_barrier_path = os.path.join(base_path, 'graphics/spaceship_strong_barrier_red_flame.png')
spaceship_red_strong_barrier_image = pygame.image.load(spaceship_red_strong_barrier_path)
spaceship_red_strong_barrier_image = pygame.transform.scale(spaceship_red_strong_barrier_image, (140, 260))

spaceship_red_weak_barrier_path = os.path.join(base_path, 'graphics/spaceship_weak_barrier_red_flame.png')
spaceship_red_weak_barrier_image = pygame.image.load(spaceship_red_weak_barrier_path)
spaceship_red_weak_barrier_image = pygame.transform.scale(spaceship_red_weak_barrier_image, (140, 260))

spaceship_red_no_barrier_path = os.path.join(base_path, 'graphics/spaceship_no_barrier_red_flame.png')
spaceship_red_no_barrier_image = pygame.image.load(spaceship_red_no_barrier_path)
spaceship_red_no_barrier_image = pygame.transform.scale(spaceship_red_no_barrier_image, (140, 260))

# spaceship with no flames indicating stopped motion of ship
spaceship_none_strong_barrier_path = os.path.join(base_path, 'graphics/spaceship_strong_barrier_no_flame.png')
spaceship_none_strong_barrier_image = pygame.image.load(spaceship_none_strong_barrier_path)
spaceship_none_strong_barrier_image = pygame.transform.scale(spaceship_none_strong_barrier_image, (140, 260))

spaceship_none_weak_barrier_path = os.path.join(base_path, 'graphics/spaceship_weak_barrier_no_flame.png')
spaceship_none_weak_barrier_image = pygame.image.load(spaceship_none_weak_barrier_path)
spaceship_none_weak_barrier_image = pygame.transform.scale(spaceship_none_weak_barrier_image, (140, 260))

spaceship_none_no_barrier_path = os.path.join(base_path, 'graphics/spaceship_no_barrier_no_flame.png')
spaceship_none_no_barrier_image = pygame.image.load(spaceship_none_no_barrier_path)
spaceship_none_no_barrier_image = pygame.transform.scale(spaceship_none_no_barrier_image, (140, 260))

asteroid_path = os.path.join(base_path, 'graphics/asteroid.png')
asteroid_image = pygame.image.load(asteroid_path)
asteroid_image = pygame.transform.scale(asteroid_image, (90, 90))

spacecow_path = os.path.join(base_path, 'graphics/spaceCow.png')
spacecow_image = pygame.image.load(spacecow_path)
spacecow_image = pygame.transform.scale(spacecow_image, (90, 90))

energy_path = os.path.join(base_path, 'graphics/energy_ball.png')
energy_image = pygame.image.load(energy_path)
energy_image = pygame.transform.scale(energy_image, (60, 60))

game_name_path = os.path.join(base_path, 'graphics/game_logo.png')
game_name = pygame.image.load(game_name_path)
game_name = pygame.transform.scale(game_name, (850, 320))

course_clear_path = os.path.join(base_path, 'graphics/game_finished.png')
course_clear = pygame.image.load(course_clear_path)
course_clear = pygame.transform.scale(course_clear, (850, 320))

game_over_path = os.path.join(base_path, 'graphics/game_over.png')
game_over = pygame.image.load(game_over_path)
game_over = pygame.transform.scale(game_over, (850, 320))

# load fonts for text
font_path = os.path.join(base_path, 'fonts/Audiowide/Audiowide-Regular.ttf')
game_font = pygame.font.Font(font_path, 35)
text_width, text_height = game_font.size('Press X to start new Game')

# initialize joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


# mapping our range <-1,1> to <0,1>
def map_range(x):
    y = (x + 1) / 2
    return y


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        self.shield_status = 2
        self.image = spaceship_strong_barrier_image
        self.surf = pygame.Surface((120, 230))
        self.rect = self.surf.get_rect(midbottom=(WIDTH / 2, HEIGHT))

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, (self.rect.centerx-72, self.rect.centery - 140))

    def move(self, x):
        # prevent spaceship from moving out of the window
        if (((x < 0) and (self.rect.left > (0 - x + 20))) or (x > 0 and (self.rect.right + x + 20) < WIDTH)):
            self.rect.move_ip(x, 0)

    def update_shield_status(self, hit):
        if hit == 'enemy':
            self.shield_status -= 1

        elif (self.shield_status < 2) and hit == 'energy':
            self.shield_status += 1

        if self.shield_status == 0:
            self.image = spaceship_no_barrier_image
        elif self.shield_status == 1:
            self.image = spaceship_weak_barrier_image
        elif self.shield_status == 2:
            self.image = spaceship_strong_barrier_image

        return self.shield_status


class Star:
    def __init__(self):
        self.radius = random.randint(1, 3)
        self.x = random.randint(1, WIDTH - 1)
        self.y = random.randint(1, HEIGHT - 1)
        # self.speed = game_speed

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.y += BACKGROUND_SPEED

    def appear_as_new_star(self):
        if self.y >= HEIGHT:
            self.y = 0
            self.x = random.randint(1, WIDTH - 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect(center=(random.randint(50, (WIDTH - 50)),
                                                  (random.randint((-HEIGHT - 300), 0))))

    def move(self, score):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, (WIDTH - 50)), (random.randint((-HEIGHT - 300), 0)))
            score += 1

        return score

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class SpaceCow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spacecow_image
        self.rect = self.image.get_rect(center=(random.randint(50, (WIDTH - 50)),
                                                (random.randint((-HEIGHT - 300), 0))))

    def move(self, score):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, (WIDTH - 50)), (random.randint((-HEIGHT - 300), 0)))
            score += 1

        return score

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class Barplot:

    def draw(self):
        #color changing according pressure
        if move_val > 0.6:
            #red
            color_tmp = (255,0,0)
        elif 0.4 < move_val < 0.7:
            #yellow
            color_tmp = (255,255,0)
        else:
            #green
            color_tmp = (124,252,0)

        #heigt changes according pressure
        height = move_val * 200

        #for addapting center of rect
        center = move_val * 200

        pygame.draw.rect(screen, color_tmp, pygame.Rect(WIDTH-100, HEIGHT-(40+center), 40, height))
        pygame.draw.rect(screen, colorBord, pygame.Rect(WIDTH-100, HEIGHT-240, 40, 200),  2)


class EnergyBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = energy_image
        self.fall = False
        self.rect = self.image.get_rect(center=(random.randint(35, (WIDTH - 35)),
                                               (random.randint((-HEIGHT - 300), 0))))

    def move(self):
        if self.fall:
            self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(35, (WIDTH - 35)), -40)
            self.fall = False

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)

    def reset(self):
        self.fall = False
        self.rect.center = (random.randint(35, (WIDTH - 35)), -40)

    def allow_movements(self):
        self.fall = True


def init_enemies():
    enemies = pygame.sprite.Group()
    for i in range(1, 7):
        enemies.add(Asteroid())

    for i in range(0, 1):
        enemies.add(SpaceCow())

    return enemies


energy = EnergyBall()
spaceship = Spaceship()
start_time = pygame.time.get_ticks()
enemy_group = init_enemies()


class GameScreen:
    def __init__(self):
        self.screen = 'intro'

    def screen_manager(self, speed):
        global energy, spaceship, start_time, enemy_group
        if self.screen == 'intro':
            energy = EnergyBall()
            spaceship = Spaceship()
            enemy_group = init_enemies()
            start_time = pygame.time.get_ticks()
            coll = True

            while coll:
                if pygame.sprite.spritecollideany(energy, enemy_group):
                    energy = EnergyBall()
                else:
                    coll = False

            self.intro_screen()
        elif self.screen == 'game_screen':
            self.game_play(speed)
        elif self.screen == 'game_over':
            self.game_over()
        elif self.screen == 'game_finished':
            self.game_finished()

    def intro_screen(self) -> None:
        global playing
        screen.fill(BLACK)
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

    def game_play(self, speed) -> None:
        global spaceship, playing, tmp, move_val, level, start_time, velocity,\
            contr, enemy_group, energy, game_speed, colorBord, color_tmp, level

        counting_time = pygame.time.get_ticks() - start_time
        events = pygame.event.get()
        hit_detected = False
        hit_type = 'enemy'
        coll = True
        #print(events)

        for event in events:
            # for controller modi
            # Condition becomes true when keyboard is pressed   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if contr == 4:
                    contr = 2
                    # print("Controller_N")
                else:
                    contr = 4
                    # print("Controller_L")

            # trigger buttons ( range -1 to 1)
            if event.type == pygame.JOYAXISMOTION:

                # left trigger pressed
                if event.axis == contr: 
                    if event.value > -1:
                        tmp = event.value
                        move_val = map_range(event.value)

                        # avoid double movements
                        if counting_time % 5 == 0:
                            # move left if button pressed in range
                            # range works only if completely new pressed
                            if move_val > 0.0 and move_val < 0.7:
                                velocity = -5
                                # print("moved left")
                            else:
                                velocity = 0
                    else:
                        velocity = 0

                # right trigger pressed
                if event.axis == 5:
                    if event.value > -1:
                        tmp = event.value
                        move_val = map_range(event.value)

                        # avoid double movements
                        if counting_time % 5 ==0: 
                            # move left if button pressed in range
                            # works only if completely new pressed
                            if 0.0 < move_val < 0.7:
                                velocity = 5
                                # print("moved right")
                            else:
                                velocity = 0
                    else:
                        velocity = 0

            if event.type == INCREASE_SPEED:
                if game_speed < 12:
                    game_speed = round(game_speed + 0.1, 1)
                #print("I am speed " + str(game_speed))

            if event.type == INCREASE_LEVEL:
                # print("I am level" + str(level))
                level += 1
                if level != 6:
                    # reset the timer for the energy balls to control the number of spawned energy per level
                    pygame.time.set_timer(SPAWN_ENERGY,
                                          int((150000 / (5 - level + 1))) + random.randint(-11000, 11000))
                # TO-DO: call here increase enemies

            if event.type == SPAWN_ENERGY:
                energy.allow_movements()

            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False

        screen.fill(BLACK)

        for star in stars:
            star.draw()
            star.move()
            star.appear_as_new_star()

        for enemy in enemy_group:
            enemy.draw()
            enemy.move(score)

        if pygame.sprite.collide_rect(spaceship, energy):
            hit_detected = True
            hit_type = 'energy'

        if pygame.sprite.spritecollide(spaceship, enemy_group, True):
            hit_detected = True
            hit_type = 'enemy'

        if hit_detected:
            if hit_type == 'enemy':
                # barrier_status = spaceship.update_shield_status('enemy')
                barrier_status = 2
                if barrier_status < 0:
                    self.screen = 'game_over'
                else:
                    rnd = random.choices(NEW_OPPONENT, OPPONENT_WEIGHTS)
                    if rnd[0] == 'asteroid':
                        enemy_group.add(Asteroid())
                    else:
                        enemy_group.add(SpaceCow())

            if hit_type == 'energy':
                energy.reset()
                while coll:
                    #print("Blello")
                    if pygame.sprite.spritecollideany(energy, enemy_group):
                        #print("I am hit in energy with enemy")
                        energy = EnergyBall()
                    else:
                        # print("I was called no collision")
                        coll = False
                barrier_status = spaceship.update_shield_status('energy')

        energy.draw()
        energy.move()
        spaceship.move(velocity)
        spaceship.draw()
        Barplot.draw(self)

        # change milliseconds into minutes, seconds
        passed_seconds = (counting_time/1000) % 60
        passed_minutes = (counting_time/(1000 * 60)) % 60

        timer = "Time: %02d:%02d" % (passed_minutes, passed_seconds)
        if counting_time >= 900000:
            self.screen = 'game_finished'

        timer_display = game_font.render(str(timer), True, WHITE)
        screen.blit(timer_display, (30, 20))
        pygame.display.update()

    def game_over(self) -> None:
        global playing

        screen.blit(game_over, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 450))
        text = game_font.render('Press X to continue', True, WHITE)
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
                    self.screen = 'intro'

    def game_finished(self) -> None:
        global playing

        screen.blit(course_clear, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 450))
        text = game_font.render('Press X to continue', True, WHITE)
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
                    self.screen = 'intro'


game_status = GameScreen()

stars = []
for i in range(200):
    stars.append(Star())

INCREASE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INCREASE_SPEED, 12000)

# add new enemies whenever a new level starts - every 3 minutes
INCREASE_LEVEL = pygame.USEREVENT + 2
pygame.time.set_timer(INCREASE_LEVEL, 180000)

# spawn energy balls regularly with a random time offset
SPAWN_ENERGY = pygame.USEREVENT + 3
# init the time depending on the level. In the first level, 5 energyballs should appear, in the 2nd level 4...
# Also create a little random offset to make it a little less predictable
pygame.time.set_timer(SPAWN_ENERGY, int((150000/(5 - level + 1))) + random.randint(-11000, 11000))

while playing:
    game_status.screen_manager(INCREASE_SPEED)
    clock.tick(FPS)

pygame.quit()

# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 
