import pygame
from images import *
import random
from pygame import mixer
speedReduction_path = os.path.join(base_path, 'sounds/speedReduction.wav')


class Spaceship(pygame.sprite.Sprite):
    
    def __init__(self, width, height):
        self.shield_status = 2
        self.speed_status = 2
        self.image = spaceship_strong_barrier_image
        self.surf = pygame.Surface((120, 230))
        self.rect = self.surf.get_rect(midbottom=(width / 2, height))

    def draw(self, screen):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, (self.rect.centerx-72, self.rect.centery - 200))
        
    def move(self, x, width):
        if self.speed_status == 0:
            x = 0
        elif self.speed_status == 1:
            x = x / 2.0
        # prevent spaceship from moving out of the window
        if (((x < 0) and (self.rect.left > (0 - x + 20))) or (x > 0 and (self.rect.right + x + 20) < width)):
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
             #game over sound
            h5 = mixer.Sound(speedReduction_path)
            h5.play()
        self.update_image()


class Star:
    def __init__(self, width, height):
        self.radius = random.randint(1, 3)
        self.x = random.randint(1, width - 1)
        self.y = random.randint(1, height - 1)
        # self.speed = game_speed

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def move(self, speed):
        self.y += speed

    def appear_as_new_star(self, width, height):
        if self.y >= height:
            self.y = 0
            self.x = random.randint(1, width - 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect(center=(random.randint(50, (width - 50)),
                                                  (random.randint((-height - 300), 0))))

    def move(self, game_speed, width, height):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > height:
            self.rect.center = (random.randint(50, (width - 50)), (random.randint((-height - 300), 0)))

    def draw(self, screen):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class SpaceCow(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = spacecow_image
        self.rect = self.image.get_rect(center=(random.randint(50, (width - 50)),
                                                (random.randint((-height - 300), 0))))

    def move(self, game_speed, width, height):
        self.rect.move_ip(0, game_speed)
        if self.rect.top > height:
            self.rect.center = (random.randint(50, (width - 50)), (random.randint((-height - 300), 0)))

    def draw(self, screen):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)


class Barplot():

    def draw(self, move, threshold, screen, color_bord, color, width, height, font, spaceship):
        # color changing according pressure
        if move > 0.6:
            color_tmp = (255, 0, 0)  # red
        elif 0.4 < move < threshold:
            color_tmp = (255, 255, 0)  # yellow
        else:
            color_tmp = (124, 252, 0)  # green

        #text = 'Pressure:'
        # label_height, label_width = font.size(text)
        #img = font.render(text, True, color)
        # for label
        #screen.blit(img, (width-250, 15))

        # heigt changes according pressure
        bar = move * 200
        # for addapting center of rect
        # center = move_val * 200
        # filling rect
        #spaceshipPos = Spaceship.get_rect()
        
        #filling
        pygame.draw.rect(screen, color_tmp, pygame.Rect(spaceship.rect.centerx - 102,
                                                        spaceship.rect.centery + 50, bar, 10))
        # border rects
        pygame.draw.rect(screen, color_bord, pygame.Rect(spaceship.rect.centerx - 102,
                                                         spaceship.rect.centery + 50, 200, 10),  2)
        pygame.draw.rect(screen, color_bord, pygame.Rect(spaceship.rect.centerx - 102,
                                                         spaceship.rect.centery + 50, 80, 10),  2)
        pygame.draw.rect(screen, color_bord, pygame.Rect(spaceship.rect.centerx - 102,
                                                         spaceship.rect.centery + 50, 120, 10),  2)
        

class EnergyBall(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = energy_image
        self.fall = False
        self.rect = self.image.get_rect(center=(random.randint(35, (width - 35)),
                                               (random.randint((-height - 300), 0))))

    def move(self, game_speed, width, height):
        if self.fall:
            self.rect.move_ip(0, game_speed)
        if self.rect.top > height:
            self.rect.center = (random.randint(35, (width - 35)), -40)
            self.fall = False

    def draw(self, screen):
        # pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        screen.blit(self.image, self.rect)

    def reset(self, width):
        self.fall = False
        self.rect.center = (random.randint(35, (width - 35)), -40)

    def allow_movements(self):
        self.fall = True
