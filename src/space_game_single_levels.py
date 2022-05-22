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
import json
from images import *
import time
import objects as obj
import argparse
from pygame import mixer
from pygame.constants import *

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (227, 65, 22)
YELLOW = (243, 219, 13)
NEW_OPPONENT = ['asteroid', 'cow']
OPPONENT_WEIGHTS = [20, 1]
BACKGROUND_SPEED = 5
FPS = 60
MAX_PRESSURE = 0.7
LEVEL_LICENCE_LIST = [bronze_licence, silver_licence,
                      gold_licence, diamond_licence, platinum_licence]
RANKS = ["Bronze", "Silver", "Gold", "Diamond", "Platinum"]

# Gerade speed-up by 10%
SETTINGS = {0: {'speed': 2.0, 'enemies': 5}, 1: {'speed': 5.1, 'enemies': 8},
            2: {'speed': 5.61, 'enemies': 9}, 3: {'speed': 6.17, 'enemies': 10},
            4: {'speed': 6.79, 'enemies': 11}, 5: {'speed': 7.47, 'enemies': 12}}


level_licence = bronze_licence
move_val = 0
velocity = 0
contr = 4
score = 0
colorBord = (131, 139, 139)
passed_time = 0
already_moved = False
counter_time = 0
playing = True
saved_data = False
LEVEL_DURATION = 120000

# Read arguments from console that decide which level is going to be played
parser = argparse.ArgumentParser()
parser.add_argument('--level', '-l', help="Which level should be started", type=int)
parser.add_argument('--output_file', '-f', help="Name of the file to which the accumulated data is saved", type=str)
args = parser.parse_args()
chosen_level = args.level
file = args.output_file


level = chosen_level
game_speed = SETTINGS[chosen_level]['speed']
number_of_enemies = SETTINGS[chosen_level]['enemies']
if level == 0:
    LEVEL_DURATION = 60000
else:
    level_licence = LEVEL_LICENCE_LIST[level - 1]

user_stats = {'user_id': file, 'level': level, 'score': 0, 'time played in ms': 0, 'number of enemy hits': 0,
              'number of energy collections': 0, 'pressure': {}}

# initialize game
pygame.init()
# display a window
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('Space Command')
clock = pygame.time.Clock()
screen.fill(BLACK)

# get width and height of screen
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
# load fonts for text
font_path = os.path.join(base_path, 'fonts/Audiowide/Audiowide-Regular.ttf')
game_font = pygame.font.Font(font_path, 35)
in_level_font = pygame.font.Font(font_path, 24)
attribution_font = pygame.font.Font(font_path, 15)
scoring_font = pygame.font.Font(font_path, 30)
text_width, text_height = game_font.size('Press X to start new Game')

# load sound and background music
intro_path = os.path.join(base_path, 'sounds/intro.wav')
enemyHit_path = os.path.join(base_path, 'sounds/hit1.wav')
energyHit_path = os.path.join(base_path, 'sounds/colectingEnergyball2.wav')

# initialize joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


# background sound
mixer.music.load(intro_path)
mixer.music.play(-1)


# mapping our range <-1,1> to <0,1>
def map_range(x):
    y = (x + 1) / 2
    return y


def init_enemies():
    enemies = pygame.sprite.Group()
    for i in range(number_of_enemies - 1):
        enemies.add(obj.Asteroid(WIDTH, HEIGHT))

    for i in range(1):
        enemies.add(obj.SpaceCow(WIDTH, HEIGHT))

    return enemies


def add_enemy(x):
    for i in range(x):
        rnd = random.choices(NEW_OPPONENT, OPPONENT_WEIGHTS)
        if rnd[0] == 'asteroid':
            enemy_group.add(obj.Asteroid(WIDTH, HEIGHT))
        else:
            enemy_group.add(obj.SpaceCow(WIDTH, HEIGHT))


def update_move_stats(val):
    global user_stats
    pressure_stats = user_stats['pressure']
    val = round(val, 2)
    if val not in pressure_stats:
        pressure_stats[val] = 1
    else:
        pressure_stats[val] += 1


def update_hit_stats(hit_type):
    global user_stats

    if hit_type == 'energy':
        user_stats['number of energy collections'] += 1
    else:
        user_stats['number of enemy hits'] += 1


def update_score_and_time(ms, scr):
    global user_stats
    user_stats['score'] = scr
    user_stats['time played in ms'] = ms


def save_user_stats():
    global saved_data
    if not saved_data:
        saved_data = True
        with open(file + '.json', 'w', encoding='utf-8') as f:
            json.dump(user_stats, f, indent=4)


def redraw_text():
    # change milliseconds into minutes, seconds
    passed_seconds = (passed_time / 1000) % 60
    passed_minutes = (passed_time / (1000 * 60)) % 60

    timer = "Time: %02d:%02d" % (passed_minutes, passed_seconds)
    timer_display = in_level_font.render(str(timer), True, WHITE)
    screen.blit(timer_display, (30, 20))
    score_str = "Score: " + str(score)
    score_display = in_level_font.render(score_str, True, WHITE)
    screen.blit(score_display, (490, 20))
    level_display = in_level_font.render("Level: " + str(level), True, WHITE)
    screen.blit(level_display, (260, 20))
    screen.blit(level_licence, (380, 15))
    pygame.display.update()


def redraw_objects(s):
    screen.fill(BLACK)

    for star in stars:
        star.draw(screen, WHITE)
        star.move(BACKGROUND_SPEED)
        star.appear_as_new_star(WIDTH, HEIGHT)

    for enemy in enemy_group:
        enemy.draw(screen)
        enemy.move(game_speed, WIDTH, HEIGHT)

    energy.draw(screen)
    energy.move(game_speed, WIDTH, HEIGHT)
    spaceship.move(velocity, WIDTH)
    spaceship.draw(screen)
    obj.Barplot.draw(s, move_val, MAX_PRESSURE, screen, colorBord, WHITE, WIDTH, HEIGHT, in_level_font, spaceship)


def display_star_background():
    screen.fill(BLACK)
    for star in stars:
        star.draw(screen, WHITE)


def display_player_results():

    level_display = game_font.render("Rank", True, RED)
    screen.blit(level_display, (WIDTH / 3, (HEIGHT / 2) + 50))

    if level > 0:
        licence = LEVEL_LICENCE_LIST[level - 1]
        screen.blit(licence, (WIDTH / 3, (HEIGHT / 2) + 130))
        rank_name = RANKS[level - 1]
        rank = scoring_font.render("/ " + rank_name, True, YELLOW)
        screen.blit(rank, (WIDTH / 3 + 50, (HEIGHT / 2) + 130))
    else:
        rank_name = "None"
        rank = scoring_font.render(rank_name, True, YELLOW)
        screen.blit(rank, (WIDTH / 3, (HEIGHT / 2) + 130))

    score_column = game_font.render("Score", True, RED)
    screen.blit(score_column, ((WIDTH / 3) + 500, (HEIGHT / 2) + 50))

    score_display = scoring_font.render(str(score), True, YELLOW)
    screen.blit(score_display, ((WIDTH / 3) + 500, (HEIGHT / 2) + 130))


class GameScreen:
    def __init__(self):
        self.screen = 'intro'

    def screen_manager(self):
        #global t0
        global energy, enemy_group
        if self.screen == 'intro':
            self.intro_screen()
        elif self.screen == 'countdown':
            #t0 = time.time()
            self.countdown_start()
        elif self.screen == 'game_screen':
            self.game_play()
        elif self.screen == 'game_over':
            save_user_stats()
            self.game_over()
        elif self.screen == 'game_finished':
            save_user_stats()
            self.game_finished()

    def intro_screen(self) -> None:
        global playing, contr
        display_star_background()

        screen.blit(game_name, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 350))
        text = in_level_font.render('Press C to select Controller Modi', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2) + 30, HEIGHT - 100))
        text = game_font.render('Press X to start new Game', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2), HEIGHT - 200))

        pygame.display.flip()

        for event in pygame.event.get():
            # for controller modi
            # Condition becomes true when keyboard is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if contr == 4:
                    contr = 2

            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
            if event.type == pygame.JOYBUTTONDOWN:
                # print(event, flush=True)
                if event.button == 0:
                    self.screen = 'countdown'

    def countdown_start(self):
        global playing, counter_time
        display_star_background()
        spaceship.draw(screen)
        obj.Barplot.draw(self, move_val, MAX_PRESSURE, screen, colorBord, WHITE, WIDTH, HEIGHT, in_level_font, spaceship)

        for event in pygame.event.get():
            # for controller modi
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
            if event.type == COUNTER:
                counter_time += 1
                if counter_time == 1:
                    screen.blit(countdown_3, ((WIDTH / 2) - (countdown_3.get_width() / 2),
                                              (HEIGHT / 2) - (countdown_3.get_height() / 2) - 150))
                    pygame.display.flip()
                elif counter_time == 2:
                    screen.blit(countdown_2, ((WIDTH / 2) - (countdown_2.get_width() / 2),
                                              (HEIGHT / 2) - (countdown_2.get_height() / 2) - 150))
                    pygame.display.flip()
                elif counter_time == 3:
                    screen.blit(countdown_1, ((WIDTH / 2) - (countdown_1.get_width() / 2),
                                              (HEIGHT / 2) - (countdown_1.get_height() / 2) - 150))
                    pygame.display.flip()
                elif counter_time == 4:
                    self.screen = 'game_screen'
                    pygame.display.flip()

    def game_play(self) -> None:
        global spaceship, playing, move_val, level, velocity,\
            enemy_group, energy, game_speed, colorBord, color_tmp, level, \
            score, passed_time, level_licence, t0, already_moved
        events = pygame.event.get()
        hit_detected = False
        hit_type = 'enemy'
        coll = True

        for event in events:
            # trigger buttons ( range -1 to 1)
            if event.type == pygame.JOYAXISMOTION:
                already_moved = True
                # left trigger pressed
                if event.axis == contr: 
                    if event.value > -1:
                        move_val = map_range(event.value)
                        update_move_stats(move_val)
                        velocity = -5
                    else:
                        velocity = 0

                # right trigger pressed
                if event.axis == 5:
                    if event.value > -1:
                        move_val = map_range(event.value)
                        update_move_stats(move_val)
                        velocity = 5
                    else:
                        velocity = 0

            # logic to decrease and increase the speed level
            t1 = time.time()
            if 0.0 < move_val < MAX_PRESSURE:
                if (t1 - t0) >= 5:
                    spaceship.update_speed_status('up')
                    t0 = time.time()
            elif already_moved and move_val >= MAX_PRESSURE:
                if (t1 - t0) >= 0.8:
                    spaceship.update_speed_status('down')
                    t0 = time.time()

            if event.type == INCREASE_TIME:
                passed_time += 1
                passed_seconds = (passed_time / 1000) % 60

                # increase the score every 2 seconds
                if passed_seconds % 2 == 0:
                    score += 1

                if passed_time >= LEVEL_DURATION:
                    extra = 100 * level * spaceship.get_shield_status()
                    score += extra
                    update_score_and_time(LEVEL_DURATION, score)
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
            update_hit_stats(hit_type)
            if hit_type == 'enemy':
                # enemy hit sound
                h1 = mixer.Sound(enemyHit_path)
                h1.play()

                barrier_status = spaceship.update_shield_status('enemy')
                # barrier_status = 2
                if barrier_status < 0:
                    update_score_and_time(passed_time, score)
                    self.screen = 'game_over'
                else:
                    add_enemy(1)

            if hit_type == 'energy':
                
                #energy hit sound
                h2 = mixer.Sound(energyHit_path)
                h2.play()

                energy.reset(WIDTH)
                while coll:
                    if pygame.sprite.spritecollideany(energy, enemy_group):
                        energy = obj.EnergyBall(WIDTH, HEIGHT)
                    else:
                        coll = False
                barrier_status = spaceship.update_shield_status('energy')

        redraw_text()

    def game_over(self) -> None:
        global playing, level

        # screen.fill(BLACK)
        display_star_background()
        screen.blit(game_over, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 400))
        display_player_results()

        text = game_font.render('Press X to quit Game', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2) + 50, HEIGHT - 200))

        attr = 'Background Music by: https://www.dl-sounds.com/royalty-free/free-game-loop2/'
        attribution = attribution_font.render(attr, True, WHITE)
        attribution_width, attribution_height = attribution_font.size(attr)
        screen.blit(attribution, (WIDTH - attribution_width - 20, HEIGHT - 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                #print(event, flush=True)
                if event.button == 0:
                    playing = False
                    pygame.quit()

    def game_finished(self) -> None:
        global playing

        display_star_background()
        screen.blit(course_clear, ((WIDTH/2) - (game_name.get_width()/2) + 20, (HEIGHT/2) - 400))
        display_player_results()

        text = game_font.render('Press X to quit Game', True, WHITE)
        screen.blit(text, ((WIDTH/2) - (text_width/2), HEIGHT - 200))

        attr = 'Background Music by: https://www.dl-sounds.com/royalty-free/free-game-loop2/'
        attribution = attribution_font.render(attr, True, WHITE)
        attribution_width, attribution_height = attribution_font.size(attr)
        screen.blit(attribution, (WIDTH - attribution_width - 20, HEIGHT - 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                # print(event, flush=True)
                if event.button == 0:
                    playing = False
                    pygame.quit()


game_status = GameScreen()
energy = obj.EnergyBall(WIDTH, HEIGHT)
spaceship = obj.Spaceship(WIDTH, HEIGHT)
enemy_group = init_enemies()

stars = []
for i in range(200):
    stars.append(obj.Star(WIDTH, HEIGHT))

INCREASE_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(INCREASE_TIME, 1)

# spawn energy balls regularly with a random time offset
SPAWN_ENERGY = pygame.USEREVENT + 2

COUNTER = pygame.USEREVENT + 3
pygame.time.set_timer(COUNTER, 1000)
# init the time depending on the level. In the first level, 5 energyballs should appear, in the 2nd level 4...
# Also create a little random offset to make it a little less predictable
if level != 0:
    pygame.time.set_timer(SPAWN_ENERGY, int((120000/(5 - level + 1))) + random.randint(-11000, 11000))
else:
    pygame.time.set_timer(SPAWN_ENERGY, 30000)
t0 = time.time()

while playing:
    game_status.screen_manager()
    clock.tick(FPS)

pygame.quit()


# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 
