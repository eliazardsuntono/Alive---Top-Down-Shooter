import pygame, random
from sys import exit
import math
from random import randint
# from pygame.sprite import _Group
from GameInfo import *
from LoadingScreen import *

pygame.init()

# WINDOW INFORMATION
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Alive")
clock = pygame.time.Clock()

# IMAGES
background = pygame.transform.scale(pygame.image.load("background/backgrounddetailed1.png").convert(), (3000, 3000))
black_bg = pygame.surface.Surface((0, 0))

def hitbox_collide(sprite1, sprite2):
    return sprite1.base_zombie_rect.colliderect(sprite2.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("sprites/Character.png").convert_alpha(), 0, PLAYER_SIZE)
        self.base_img = self.image
        self.hitbox_rect = self.base_img.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y )
        self.health = 100
    
    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        
        keys = pygame.key.get_pressed()
        
        #MOVEMENT
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
            
        #SHOOTING
        if pygame.mouse.get_pressed() == (1,0,0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
            
    def is_shooting(self):
         if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            SPAWN_POS = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(SPAWN_POS[0], SPAWN_POS[1], self.angle)
            bullets.add(self.bullet)
            all_sprites.add(self.bullet)
            
    
    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_distance = (self.mouse_pos[0] - WIDTH // 2)
        self.y_distance = (self.mouse_pos[1] - HEIGHT // 2)
        
        self.angle = math.degrees(math.atan2(self.y_distance, self.x_distance))
        self.image = pygame.transform.rotate(self.base_img, -self.angle)
        
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
    
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        
    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.background = background
        self.floor_rect = background.get_rect(topleft=(0,0))

    def custom_draw(self, screen, player):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(self.background, floor_offset_pos)

        for sprite in all_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemies, all_sprites)

        zombie_info = monster_data["zombie"]
        self.health = zombie_info["health"]
        self.image_scale = zombie_info["image_scale"]
        self.image = zombie_info["image"].convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.image_scale)
        self.image_mask = pygame.mask.from_surface(self.image)
        self.base_img = self.image
        self.attack_damage = zombie_info["attack_damage"]
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = randint(3,8)

        self.position = pygame.math.Vector2(position)
        
        self.hitbox_rect = zombie_info["hitbox_rect"]
        self.base_zombie_rect = self.hitbox_rect.copy()
        self.base_zombie_rect.center = self.rect.center
        
        self.collide = False

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def is_alive(self):
        return self.health > 0
        
    def zombie_rotation(self):
        player_x = player.rect.x
        zombie_x = self.rect.x
        x_dist = zombie_x - player_x
        
        player_y = player.rect.y
        zombie_y = self.rect.y
        y_dist = player_y - zombie_y
        
        self.angle = math.degrees(math.atan2(x_dist, y_dist))
        self.image = pygame.transform.rotate(self.base_img, -self.angle)
        
    def update(self):
        global score_count
        global score
        global text
        global wave_count
        global wave
        global multiplier
        
        if self.is_alive():
            self.hunt_player()
            self.zombie_rotation()
            text = font.render(f'Zombies Left: {len(enemies)}', True, (0, 0, 0))
            # Check for collision with player
            if hitbox_collide(self, player):
                player.health -= self.attack_damage
                # Check if player's health goes below zero
                if player.health <= 0:
                    pass 
                else:
                    health_bar.current_health = player.health
                    health_bar.update()

        else:
            self.kill()
            
            # Updates the score in reference to how many zombies killed
            score_count += 100
            score = font.render(f'Score: {score_count}', True, (0,0,0))

            # Updates Wave Number 
            wave = font.render(f'Wave: {wave_count}', True, (0,0,0))
            
            # update text to show how many zombies are left
            text = font.render(f'Zombies Left: {len(enemies)}', True, (0, 0, 0))
            if len(enemies) == 0: 
                wave_count += 1 
                wave = font.render(f'Wave: {wave_count}', True, (0,0,0))
                multiplier += 1 
                for _ in range((ENEMY_SPAWN_COUNT*multiplier)):
                    enemies.add(Enemy((random.randint(0, 3000), random.randint(0, 3000))))

    def get_vector_distance(self, x, y):
        return (x - y).magnitude()    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("assets/bullet.png").convert_alpha(), 0, BULLET_SCALING)

        self.image_mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = x
        self.y = y

        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_speed = math.cos(self.angle * (2 * math.pi/360)) * self.speed
        self.y_speed = math.sin(self.angle * (2 * math.pi/360)) * self.speed
        
        # WE CAN ADJUST TO LENGTHEN HOW FAR THE BULLET GOES
        self.bullet_life = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        
    def bullet_move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_life:
            self.kill() 
    
    def bullet_collisions(self): 
        global text

        for enemy in pygame.sprite.spritecollide(self, enemies, False):
            if enemy.image_mask.overlap(self.image_mask, (self.x - enemy.rect.x, self.y - enemy.rect.y)):
                enemy.health -= 10
                # print("collision detected")

                # bullet despawns once it hits something
                self.kill()
                return
    
    def update(self):
        self.bullet_move()
        self.bullet_collisions()

class HealthBar:
    global screen
    def __init__(self):
        self.current_health = 100
        self.maximum_health = 100
        self.health_bar_size = 100
        self.health_ratio = self.maximum_health / self.health_bar_size
        self.current_colour = None

    def display_health_bar(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (10, 15, self.health_bar_size * 3, 20))

        if self.current_health >= 75:
            pygame.draw.rect(surface, (0, 255, 0), (10, 15, self.current_health * 3, 20))
            self.current_colour = (0, 255, 0)
        elif self.current_health >= 50:
            pygame.draw.rect(surface, (255, 255, 0), (10, 15, self.current_health * 3, 20))
            self.current_colour = (255, 255, 0)
        elif self.current_health >= 0:
            pygame.draw.rect(surface, (255, 0, 0), (10, 15, self.current_health * 3, 20))
            self.current_colour = (255, 0, 0)

        pygame.draw.rect(surface, (255, 255, 255), (10, 15, self.health_bar_size * 3, 20), 4)

    def display_health_number(self): 
        health_surface = font.render(f'{player.health} / {self.maximum_health}', False, self.current_colour)
        health_rect = health_surface.get_rect(center=(410, 25))
        screen.blit(health_surface, health_rect)


    def update(self):
        self.display_health_bar(screen)
        self.display_health_number()
        
        

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

camera = Camera()
player = Player()
health_bar = HealthBar()

# spawn in zombies randomly
for _ in range(ENEMY_SPAWN_COUNT):
    enemies.add(Enemy((random.randint(0, 3000), random.randint(0, 3000))))

all_sprites.add(player)
all_sprites.add(enemies) 

# for writing text on the top right
font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render(f'Zombies Left: {len(enemies)}', True, (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (WIDTH - 150, 60)


score_count = 0
score = font.render(f'Score: {score_count}', True, (0,0,0))
score_rect = score.get_rect()
score_rect.center = (WIDTH - 150, 90)

wave_count = 1
wave = font.render(f'Wave: {wave_count}', True, (0,0,0))
wave_rect = wave.get_rect()
wave_rect.center = (WIDTH - 150, 30)

multiplier = 1

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill((0, 0, 0))
    camera.custom_draw(screen, player)

    all_sprites.update()
    health_bar.update() 
    
    # Check if player's health is zero or less
    if player.health <= 0:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.quit()
        exit()
    else:
        health_bar.display_health_bar(screen)
        health_bar.display_health_number()   
        screen.blit(wave, wave_rect)
        screen.blit(text, text_rect)
        screen.blit(score, score_rect)
    
    pygame.display.update()
    clock.tick(60)

