import pygame
from random import randint

WIDTH = 1280
HEIGHT = 720

#PLAYER INFO
PLAYER_START_X = 1000
PLAYER_START_Y = 1000
PLAYER_SIZE = 0.5
PLAYER_SPEED = 10
GUN_OFFSET_X = 65
GUN_OFFSET_Y = 24 

#BULLET SETTINGS
SHOOT_COOLDOWN = 20
BULLET_SCALING = 1.2
BULLET_SPEED = 10
BULLET_LIFETIME = 750

# COLOR TUPLES
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#ENEMY INFO
ENEMY_SPAWN_COUNT = 10
monster_data = {
    "zombie": {"health": randint(1,30) , "attack_damage": 20, "image": pygame.image.load("sprites/Zombie.png"), "image_scale": 0.40, "hitbox_rect": pygame.Rect(0,0,75,100)},
}
