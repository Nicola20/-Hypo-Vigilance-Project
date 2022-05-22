import pygame
import os

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

spacecow_path = os.path.join(base_path, 'graphics/spaceCow2.png')
spacecow_image = pygame.image.load(spacecow_path)
spacecow_image = pygame.transform.scale(spacecow_image, (90, 90))

energy_path = os.path.join(base_path, 'graphics/energy_ball.png')
energy_image = pygame.image.load(energy_path)
energy_image = pygame.transform.scale(energy_image, (60, 60))

# level badge images
bronze_path = os.path.join(base_path, 'graphics/licence_bronze.png')
bronze_licence = pygame.image.load(bronze_path)
bronze_licence = pygame.transform.scale(bronze_licence, (41, 41))

silver_path = os.path.join(base_path, 'graphics/licence_silver.png')
silver_licence = pygame.image.load(silver_path)
silver_licence = pygame.transform.scale(silver_licence, (41, 41))

gold_path = os.path.join(base_path, 'graphics/licence_gold.png')
gold_licence = pygame.image.load(gold_path)
gold_licence = pygame.transform.scale(gold_licence, (41, 41))

diamond_path = os.path.join(base_path, 'graphics/licence_diamond.png')
diamond_licence = pygame.image.load(diamond_path)
diamond_licence = pygame.transform.scale(diamond_licence, (41, 41))

platinum_path = os.path.join(base_path, 'graphics/licence_platinum.png')
platinum_licence = pygame.image.load(platinum_path)
platinum_licence = pygame.transform.scale(platinum_licence, (41, 41))

# game text
game_name_path = os.path.join(base_path, 'graphics/game_logo.png')
game_name = pygame.image.load(game_name_path)
game_name = pygame.transform.scale(game_name, (850, 320))

course_clear_path = os.path.join(base_path, 'graphics/game_finished.png')
course_clear = pygame.image.load(course_clear_path)
course_clear = pygame.transform.scale(course_clear, (850, 320))

game_over_path = os.path.join(base_path, 'graphics/game_over.png')
game_over = pygame.image.load(game_over_path)
game_over = pygame.transform.scale(game_over, (850, 320))

countdown_3_path = os.path.join(base_path, 'graphics/countdown_3.png')
countdown_3 = pygame.image.load(countdown_3_path)
img_size = countdown_3.get_size()
countdown_3 = pygame.transform.scale(countdown_3, (img_size[0] - 100, img_size[1] - 100))

countdown_2_path = os.path.join(base_path, 'graphics/countdown_2.png')
countdown_2 = pygame.image.load(countdown_2_path)
img_size = countdown_2.get_size()
countdown_2 = pygame.transform.scale(countdown_2, (img_size[0] - 100, img_size[1] - 100))

countdown_1_path = os.path.join(base_path, 'graphics/countdown_1.png')
countdown_1 = pygame.image.load(countdown_1_path)
img_size = countdown_1.get_size()
countdown_1 = pygame.transform.scale(countdown_1, (img_size[0] - 100, img_size[1] - 100))
