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

# constants
# BACKGROUND_SPEED = 2
FPS = 60

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
game_speed = 5
level = 1
score = 0


# load images
base_path = os.path.dirname(__file__)
spaceship_strong_barrier_path = os.path.join(base_path, 'graphics/spaceship_strong_barrier.png')
spaceship_strong_barrier_image = pygame.image.load(spaceship_strong_barrier_path)
spaceship_strong_barrier_image = pygame.transform.scale(spaceship_strong_barrier_image, (140, 260))

spaceship_weak_barrier_path = os.path.join(base_path, 'graphics/spaceship_weak_barrier.png')
spaceship_weak_barrier_image = pygame.image.load(spaceship_weak_barrier_path)
spaceship_weak_barrier_image = pygame.transform.scale(spaceship_weak_barrier_image, (140, 260))

spaceship_no_barrier_path = os.path.join(base_path, 'graphics/spaceship_no_barrier.png')
spaceship_no_barrier_image = pygame.image.load(spaceship_no_barrier_path)
spaceship_no_barrier_image = pygame.transform.scale(spaceship_no_barrier_image, (140, 260))

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
        self.surf = pygame.Surface((110, 230))
        self.rect = self.surf.get_rect(midbottom=(WIDTH / 2, HEIGHT))

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
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
            self.image == spaceship_no_barrier_image
        elif self.shield_status == 1:
            self.image == spaceship_weak_barrier_image
        elif self.shield_status == 2:
            self.image == spaceship_strong_barrier_image

        print("I am shield " + str(self.shield_status))
        return self.shield_status


class Star:
    def __init__(self, x, y, speed):
        self.radius = random.randint(1, 3)
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


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect(center=(random.randint(95, (WIDTH - 95)),
                                                  (random.randint((-HEIGHT - 300), 0))))

    def move(self, score):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(95, (WIDTH - 95)), (random.randint((-HEIGHT - 300), 0)))
            score += 1

        return score

    def draw(self, surface):
        pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        surface.blit(self.image, self.rect)


class SpaceCow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spacecow_image
        self.rect = self.image.get_rect(center=(random.randint(95, (WIDTH - 95)),
                                                (random.randint((-HEIGHT - 300), 0))))

    def move(self, score):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(95, (WIDTH - 95)), (random.randint((-HEIGHT - 300), 0)))
            score += 1

        return score

    def draw(self, surface):
        pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        surface.blit(self.image, self.rect)


class EnergyBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = energy_image
        self.rect = self.image.get_rect(center=(random.randint(65, (WIDTH - 65)),
                                               (random.randint((-HEIGHT - 300), 0))))

    def move(self):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(65, (WIDTH - 65)), 0)

    def draw(self, surface):
        pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        surface.blit(self.image, self.rect)


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

    def screen_manager(self):
        global energy, spaceship, start_time, enemy_group
        if self.screen == 'intro':
            energy = EnergyBall()
            spaceship = Spaceship()
            enemy_group = init_enemies()
            start_time = pygame.time.get_ticks()
            self.intro_screen()
        elif self.screen == 'game_screen':
            self.game_play()
        elif self.screen == 'game_over':
            self.game_over()

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


    def game_play(self) -> None:
        global spaceship, playing, tmp, move_val, level, start_time, velocity,contr
        counting_time = pygame.time.get_ticks() - start_time
        events = pygame.event.get()
        #print(events)
        # game_status.game_play(ship_x)
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
                        if counting_time % 5 ==0: 
                            # move left if button pressed in range
                            if move_val > 0.0 and move_val < 0.7:  # range works only if comletely new pressed
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
                            if move_val > 0.0 and move_val < 0.7:  # range works only if comletely new pressed
                                velocity = 5
                                # print("moved right")
                            else:
                                velocity = 0
                    else:
                        velocity = 0

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
            enemy.draw(screen)
            enemy.move(score)

        energy.draw(screen)
        energy.move()

        # move space ship
        spaceship.move(velocity)
        spaceship.draw()

        if pygame.sprite.collide_rect(spaceship, energy):
            barrier_status = spaceship.update_shield_status('enery')

        if pygame.sprite.spritecollideany(spaceship, enemy_group):
            # self.screen == 'game_over'
            print("collision")
            barrier_status = spaceship.update_shield_status('enemy')
            if barrier_status < 0:
                self.screen = 'game_over'

        # change milliseconds into minutes, seconds
        passed_seconds = (counting_time/1000) % 60
        passed_minutes = (counting_time/(1000 * 60)) % 60

        timer = "Time: %02d:%02d" % (passed_minutes, passed_seconds)

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


game_status = GameScreen()

stars = []
for i in range(200):
    x_pos = random.randint(1, WIDTH - 1)
    y_pos = random.randint(1, HEIGHT - 1)
    stars.append(Star(x_pos, y_pos, game_speed))


while playing:
    game_status.screen_manager()
    clock.tick(FPS)

pygame.quit()

# for evaluating the stress level:
# could save the button values in array ---> calculating avarage 
# or display range higher deflection ---> higher stress level 
