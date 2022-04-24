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
from images import *
import time
#import numpy as np
#import matplotlib.pyplot as plt
from pygame import mixer
from pygame.constants import *

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEW_OPPONENT = ['asteroid', 'cow']
OPPONENT_WEIGHTS = [20, 1]
BACKGROUND_SPEED = 5
FPS = 60
NUM_OF_LEVELS = 5
LEVEL_LICENCE_LIST = [bronze_licence, silver_licence,
                      gold_licence, diamond_licence, platinum_licence]

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
level_licence = bronze_licence
score = 0
colorBord = (131, 139, 139)
color_tmp = (124, 252, 0)
height = 0
passed_time = 0

# load fonts for text
font_path = os.path.join(base_path, 'fonts/Audiowide/Audiowide-Regular.ttf')
game_font = pygame.font.Font(font_path, 35)
in_level_font = pygame.font.Font(font_path, 25)
text_width, text_height = game_font.size('Press X to start new Game')

#load sound and background music
intro_path = os.path.join(base_path, 'sounds/intro.wav')

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
        self.speed_status = 2
        self.image = spaceship_strong_barrier_image
        self.surf = pygame.Surface((120, 230))
        self.rect = self.surf.get_rect(midbottom=(WIDTH / 2, HEIGHT))

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, (self.rect.centerx-72, self.rect.centery - 140))

    def move(self, x):
        if self.speed_status == 0:
            x = 0
        elif self.speed_status == 1:
            x = x / 2.0
        # prevent spaceship from moving out of the window
        if (((x < 0) and (self.rect.left > (0 - x + 20))) or (x > 0 and (self.rect.right + x + 20) < WIDTH)):
            self.rect.move_ip(x, 0)

    def update_image(self):
        if self.shield_status == 0:
            if self.speed_status == 2:
                self.image = spaceship_no_barrier_image
            if self.speed_status == 1:
                self.image = spaceship_red_no_barrier_image
            if self.speed_status == 0:
                self.image = spaceship_none_no_barrier_image
        elif self.shield_status == 1:
            if self.speed_status == 2:
                self.image = spaceship_weak_barrier_image
            if self.speed_status == 1:
                self.image = spaceship_red_weak_barrier_image
            if self.speed_status == 0:
                self.image = spaceship_none_weak_barrier_image
        elif self.shield_status == 2:
            if self.speed_status == 2:
                self.image = spaceship_strong_barrier_image
            if self.speed_status == 1:
                self.image = spaceship_red_strong_barrier_image
            if self.speed_status == 0:
                self.image = spaceship_none_strong_barrier_image

    def update_shield_status(self, hit):
        if hit == 'enemy':
            self.shield_status -= 1

        elif (self.shield_status < 2) and hit == 'energy':
            self.shield_status += 1

        self.update_image()
        return self.shield_status

    def get_shield_status(self):
        return self.shield_status

    def update_speed_status(self, react):
        if react == 'up' and self.speed_status < 2:
            self.speed_status += 1
        elif react == 'down' and self.speed_status > 0:
            self.speed_status -= 1
        self.update_image()


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

    def move(self):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, (WIDTH - 50)), (random.randint((-HEIGHT - 300), 0)))

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class SpaceCow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spacecow_image
        self.rect = self.image.get_rect(center=(random.randint(50, (WIDTH - 50)),
                                                (random.randint((-HEIGHT - 300), 0))))

    def move(self):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, (WIDTH - 50)), (random.randint((-HEIGHT - 300), 0)))

    def draw(self):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class Barplot:

    def draw(self):
        # color changing according pressure
        if move_val > 0.6:
            color_tmp = (255, 0, 0)  # red
        elif 0.4 < move_val < 0.7:
            color_tmp = (255, 255, 0)  # yellow
        else:
            color_tmp = (124, 252, 0)  # green

        # heigt changes according pressure
        height = move_val * 200
        # for addapting center of rect
        # center = move_val * 200
        # filling rect
        pygame.draw.rect(screen, color_tmp, pygame.Rect(WIDTH-250, HEIGHT-810, height, 40))
        # border rect
        pygame.draw.rect(screen, colorBord, pygame.Rect(WIDTH-250, HEIGHT-810, 200, 40),  2)

        # for label
        font = pygame.font.SysFont(None, 30)
        img = font.render('Pressure:', True, WHITE)
        screen.blit(img, (WIDTH-250, HEIGHT-832))


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
    for i in range(1, 9):
        enemies.add(Asteroid())

    for i in range(0, 1):
        enemies.add(SpaceCow())

    return enemies


def add_enemy(x):
    for i in range(x):
        rnd = random.choices(NEW_OPPONENT, OPPONENT_WEIGHTS)
        if rnd[0] == 'asteroid':
            enemy_group.add(Asteroid())
        else:
            enemy_group.add(SpaceCow())


def redraw_text():
    # change milliseconds into minutes, seconds
    passed_seconds = (passed_time / 1000) % 60
    passed_minutes = (passed_time / (1000 * 60)) % 60

    timer = "Time: %02d:%02d" % (passed_minutes, passed_seconds)
    timer_display = in_level_font.render(str(timer), True, WHITE)
    screen.blit(timer_display, (30, 20))
    score_str = "Score: " + str(score)
    score_display = in_level_font.render(score_str, True, WHITE)
    screen.blit(score_display, (260, 20))
    level_display = in_level_font.render("Level: " + str(level), True, WHITE)
    screen.blit(level_display, (440, 20))
    screen.blit(level_licence, (560, 15))
    pygame.display.update()


def redraw_objects(s):
    screen.fill(BLACK)

    for star in stars:
        star.draw()
        star.move()
        star.appear_as_new_star()

    for enemy in enemy_group:
        enemy.draw()
        enemy.move()

    energy.draw()
    energy.move()
    spaceship.move(velocity)
    spaceship.draw()
    Barplot.draw(s)


energy = EnergyBall()
spaceship = Spaceship()
enemy_group = init_enemies()


class GameScreen:
    def __init__(self):
        self.screen = 'intro'

    def screen_manager(self):
        global energy, spaceship, enemy_group
        if self.screen == 'intro':
            energy = EnergyBall()
            spaceship = Spaceship()
            enemy_group = init_enemies()
            #start_time = pygame.time.get_ticks()
            coll = True

            while coll:
                if pygame.sprite.spritecollideany(energy, enemy_group):
                    energy = EnergyBall()
                else:
                    coll = False

            self.intro_screen()
        elif self.screen == 'game_screen':
            self.game_play()
        elif self.screen == 'game_over':
            self.game_over()
        elif self.screen == 'game_finished':
            self.game_finished()

    def intro_screen(self) -> None:
        global playing
        screen.fill(BLACK)
        screen.blit(game_name, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 350))
        text = game_font.render('Press X to start new Game', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2), HEIGHT - 200))
        #background sound
        #mixer.music.load(intro_path)
        #print("music loaded")
        #mixer.music.play(-1)

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
        global spaceship, playing, tmp, move_val, level, velocity,\
            contr, enemy_group, energy, game_speed, colorBord, color_tmp, level, \
            score, passed_time, level_licence
        events = pygame.event.get()
        hit_detected = False
        hit_type = 'enemy'
        coll = True

        for event in events:
            # for controller modi
            # Condition becomes true when keyboard is pressed   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if contr == 4:
                    contr = 2

            # trigger buttons ( range -1 to 1)
            if event.type == pygame.JOYAXISMOTION:
                # left trigger pressed
                if event.axis == contr: 
                    if event.value > -1:
                        tmp = event.value
                        move_val = map_range(event.value)

                        # avoid double movements
                        if passed_time % 1 == 0:
                            # move left if button pressed in range
                            # works only if completely new pressed
                            if 0.0 < move_val < 0.7:
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
                        if passed_time % 1 == 0:
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

            if event.type == INCREASE_TIME:
                passed_time += 1
                passed_seconds = (passed_time / 1000) % 60
                passed_minutes = (passed_time / (1000 * 60)) % 60

                # increase the score every 3 seconds
                if passed_seconds % 3 == 0:
                    score += 1

                # increase the level every 3 minutes
                if passed_minutes % 3 == 0:
                    level += 1
                    if level != 6:
                        # reset the timer for the energy balls to control the number of spawned energy per level
                        pygame.time.set_timer(SPAWN_ENERGY,
                                              int((150000 / (5 - level + 1))) + random.randint(-11000, 11000))

                        # increase the enemies
                        # if level != 5:
                        add_enemy(1)
                        # update the level symbol
                        level_licence = LEVEL_LICENCE_LIST[level - 1]

                    extra = 100 * level * spaceship.get_shield_status()
                    for i in range(extra):
                        score += 1
                        redraw_objects(self)
                        redraw_text()
                        # pygame.time.delay(2)

                if passed_time >= 900000:
                    self.screen = 'game_finished'

            if event.type == SPAWN_ENERGY:
                energy.allow_movements()

            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False

        redraw_objects(self)

        if pygame.sprite.collide_rect(spaceship, energy):
            hit_detected = True
            hit_type = 'energy'

        if pygame.sprite.spritecollide(spaceship, enemy_group, True):
            hit_detected = True
            hit_type = 'enemy'

        if hit_detected:
            if hit_type == 'enemy':
                barrier_status = spaceship.update_shield_status('enemy')
                # barrier_status = 2
                if barrier_status < 0:
                    self.screen = 'game_over'
                else:
                    add_enemy(1)

            if hit_type == 'energy':
                energy.reset()
                while coll:
                    if pygame.sprite.spritecollideany(energy, enemy_group):
                        energy = EnergyBall()
                    else:
                        coll = False
                barrier_status = spaceship.update_shield_status('energy')

        redraw_text()

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

INCREASE_TIME = pygame.USEREVENT + 2
pygame.time.set_timer(INCREASE_TIME, 1)

# spawn energy balls regularly with a random time offset
SPAWN_ENERGY = pygame.USEREVENT + 3
# init the time depending on the level. In the first level, 5 energyballs should appear, in the 2nd level 4...
# Also create a little random offset to make it a little less predictable
pygame.time.set_timer(SPAWN_ENERGY, int((150000/(5 - level + 1))) + random.randint(-11000, 11000))
t0 = time.time()

while playing:
    game_status.screen_manager()
    clock.tick(FPS)

pygame.quit()

# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 
