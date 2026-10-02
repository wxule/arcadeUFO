from threading import Timer

import pygame as pg
import random
import math
import time
import schedule
import sys

from pygame import display

clock = pg.time.Clock()
pg.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (92, 194, 91)
NICE_GREEN = (112, 196, 118)
RED = (194, 51, 25)
NICE_RED = (219, 121, 121)
NICE_TEAL = (119, 146, 189)
NICE_BRIGHT_YELLOW = (251, 255, 222)



window_width = 500
window_height = 700
window = pg.display.set_mode((window_width, window_height))
window.fill(NICE_TEAL)
background = pg.image.load("background.png")
background = pg.transform.scale(background, (500, 700))
font = pg.font.Font("PressStart2P.ttf", 15)

win = pg.image.load("YOU WIN.png")
win = pg.transform.scale(win, (500, 700))

win_sound = pg.mixer.Sound("win.mp3")
win_sound.set_volume(0.1)


lose_sound = pg.mixer.Sound("lose.mp3")
lose_sound.set_volume(0.1)

pg.mixer.music.load("2d beat.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)

hit_sound = pg.mixer.Sound('punch.mp3')
hit_sound.set_volume(0.03)

destroy_sound = pg.mixer.Sound("hit.mp3")
destroy_sound.set_volume(0.03)

class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, x_size, y_size, image_path):
        super().__init__()
        self.color = RED
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (x_size, y_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_as_rect(self):
        pg.draw.rect(window, self.color, self.rect)

    def draw_image(self):
        window.blit(self.image, self.rect)

class Platform(Sprite):

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.rect.left > 0:
            self.rect.x -= 5
        elif keys[pg.K_d] and self.rect.right < 500:
            self.rect.x += 5



class Ball(Sprite):
    def __init__(self, x, y, x_size, y_size, image_path):
        super().__init__(x, y, x_size, y_size, image_path)
        self.angle = 0
        self.rotation_speed = 3
        self.original_image = self.image.copy().convert_alpha()
        self.speed_x = 5
        self.speed_y = 5
        self.is_collided = True


    def update(self):
        self.angle += self.rotation_speed % 360
        self.image = pg.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right >= window_width - 15 or self.rect.left <= 15:
            hit_sound.play()
            self.speed_x *= -1

        if self.rect.top <= 0:
            hit_sound.play()
            self.speed_y *= -1

        if self.rect.bottom >= window_height:
            self.rect.x = 50
            self.rect.y = 300


        if pg.sprite.collide_rect(self, platform) and self.is_collided:
            hit_sound.play()
            self.speed_y *= -1
            self.is_collided = False
            Timer(1.0, lambda: setattr(self, "is_collided", True)).start()



    def draw_as_rect(self):
        pg.draw.circle(window, self.color, self.rect.center, radius=20)



class Enemy(Sprite):
    def __init__(self, x, y, x_size, y_size, image_path, color):
        super().__init__(x, y, x_size, y_size, image_path)

        self.color = color
        self.rect = pg.Rect(x, y, x_size, y_size)










ball = Ball(400, 300, 50, 50, "ball.png")

window.blit(background, (0, 0))
platform = Platform(200, 550, 100, 20, "plate.png")


enemies = pg.sprite.Group()

for b in range(3):
    for i in range(4):
        enemy = Enemy(30 + i * 120, 60 + b * 70, 90, 40, "enemies.png", RED)
        enemies.add(enemy)




score = 0000

game_won = False
while True:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if not game_won:

        window.blit(background, (0, 0))




        ball.draw_as_rect()
        ball.draw_image()
        ball.update()

        for enemy in enemies:
            enemy.draw_image()

        #platform.draw_as_rect()
        platform.draw_image()
        platform.update()
        contact = pg.sprite.spritecollide(ball, enemies, True)
        if contact:
            ball.speed_y *= -1
            destroy_sound.play()
            for element in contact:
                score += 100


        score_calc = font.render(f"{score:04d}", 1, WHITE)

        window.blit(score_calc, (222, 678))

        if score >= 1200:
            win_sound.play()
            game_won = True

    else:
        window.blit(win, (0, 0))







    pg.display.update()