#USE LINK:
#https://replit.com/@bchian316/Space-Invaders?lite=1&outputonly=1#main.py
import pygame
import random
from time import time, sleep
from sys import stdout, exit
from os import system
from math import sqrt, atan, degrees
from termcolor import cprint
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
game_is_running = True
status = "playing"
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ship.png")
pygame.display.set_icon(icon)
mouse_position = pygame.mouse.get_pos()
mouse_position = list(mouse_position)
playerx = 250
playery = 400
player_speed = 5
fire_speed = 0.1
lives = 0
starting_lives = 5
money = 0
money_img = pygame.image.load("money.png")
player = pygame.image.load("ship.png")
enemy_img = pygame.image.load("ghost.png")
life_img = pygame.image.load("heart.png")
earth_img = pygame.image.load("planet-earth.png")
spawner_img = pygame.image.load("ufo.png")
shooter_img = pygame.image.load("spaceship.png")
shooter_img = pygame.transform.rotate(shooter_img, 180)
miniboss_img = pygame.image.load("miniboss.png")
miniboss_img = pygame.transform.rotate(miniboss_img, 180)
mouse_up = True
mouse_down = False
mouse_clicked = False
unavailable_btn_color = (145, 145, 145, 145)
available_btn_color = (0, 255, 0)
hover_available_btn_color = (43, 186, 43)
def text(size, message, color, textx, texty, align = "left", font = "Comic Sans MS"):
  myfont = pygame.font.SysFont(font, size)
  text_width, text_height = myfont.size(message)
  text_surface = myfont.render(message, True, color)
  if align == "left":
    screen.blit(text_surface, (textx, texty))
  if align == "center":
    screen.blit(text_surface, (textx - (text_width/2), texty))
  if align == "right":
    screen.blit(text_surface, (textx - text_width, texty))
def collided(x1, y1, length1, height1, x2, y2, length2, height2):
  #1 = object
  #2 = target
  if x1 >= x2 - length1 and x1 <= x2 + length2 and y1 >= y2 - height1 and y1 <= y2 + height2:
    return True
  return False
class Life:
  global life_img
  _list = []
  def __init__(self):
    global lives
    self.x = 750 + (lives * 35)
    self.img = life_img
  def update(self):
    global lives
    screen.blit(self.img, (self.x, 0))
for _ in range(starting_lives):
  Life._list.append(Life())
  lives += 1
class Bullet:
  _list = []
  speed = 5
  damage = 1
  def __init__(self):
    global playerx
    global playery
    global screen
    self.index_number = len(Bullet._list) - 1
    self.bulletx = playerx + 11
    self.bullety = playery
    self.bulletsize = 8
    pygame.draw.rect(screen, (255, 0, 0), (self.bulletx, self.bullety, self.bulletsize, self.bulletsize))
  def update(self):
    global screen
    self.bullety -= Bullet.speed
    pygame.draw.rect(screen, (255, 0, 0), (self.bulletx, self.bullety, self.bulletsize, self.bulletsize))
    if self.bullety < 0:
      Bullet._list.pop(self.index_number)
class Enemybullet:
  _list = []
  speed = 1.5
  def __init__(self, index_number):
    global playerx
    global playery
    global screen
    self.index_number = len(Enemybullet._list) - 1
    self.bulletx = Shooter._list[index_number].x + 18
    self.bullety = Shooter._list[index_number].y + 48
    self.bulletsize = 12
    pygame.draw.rect(screen, (255, 0, 0), (self.bulletx, self.bullety, self.bulletsize, self.bulletsize))
  def update(self):
    global screen
    global lives
    global playerx
    global playery
    self.bullety += Enemybullet.speed
    pygame.draw.rect(screen, (0, 0, 255), (self.bulletx, self.bullety, self.bulletsize, self.bulletsize))
    if self.bullety > 1000:
      Enemybullet._list.pop(self.index_number)
    if collided(playerx, playery, 32, 32, self.bulletx, self.bullety, self.bulletsize, self.bulletsize):
      lives -= 1
      Life._list.pop(-1)
      Enemybullet._list.pop(self.index_number)
class Enemy:
  _list = []
  speed = 0.25
  reward = 1
  time = 15
  def __init__(self, x = None, y = -42):
    global screen
    x = random.randint(0, 968)
    self.lives = 1
    self.x = x
    self.y = y
    self.image = enemy_img
    self.index_number = len(Enemy._list) - 1
    self.start_time = time()
    self.end_time = time()
    screen.blit(self.image, (self.x, self.y))
  def update(self):
    global playerx
    global playery
    global lives
    global money
    self.y += 0.25
    if self.y < playery + 32:
      if self.x > playerx:
        self.x -= Enemy.speed
      if self.x < playerx:
        self.x += Enemy.speed
    screen.blit(self.image, (self.x, self.y))
    pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + 36, 32, 10))
    text(15, str(self.lives), (0, 0, 0), self.x + 16, self.y + 36, align = "center")
    if self.y > 1000:
      Enemy._list.pop(self.index_number) 
    if collided(playerx, playery, 32, 32, self.x, self.y, 32, 32):
      lives -= 1
      Life._list.pop(-1)
      Enemy._list.pop(self.index_number)
    for _ in Bullet._list:
      if collided(self.x, self.y, 32, 32, _.bulletx, _.bullety, _.bulletsize, _.bulletsize):
        self.lives -= Bullet.damage
        Bullet._list.remove(_)
    if self.lives <= 0:
      Enemy._list.pop(self.index_number)
      money += Enemy.reward
class Spawner:
  _list = []
  spawn_time = 2
  speed = 0.5
  reward = 10
  time = 45
  def __init__(self):
    global spawner_img
    self.img = spawner_img
    self.direction = random.choice(["left", "right"])
    self.lives = 5
    self.x = random.randint(0, 936)
    self.y = -148
    self.stopy = random.randint(50, 150)
    self.index_number = len(Spawner._list) - 1
    self.start_time = time()
    self.end_time = time()
    screen.blit(self.img, (self.x, self.y))
  def update(self):
    global money
    if self.y < self.stopy:
      self.y += Spawner.speed
    else:
      if self.direction == "left":
        self.x -= Spawner.speed
        if self.x < 0:
          self.direction = "right"
      else:
        self.x += Spawner.speed
        if self.x > 936:
          self.direction = "left"
    pygame.draw.rect(screen, (0, 255, 0), (self.x + 3, self.y + 96, 18 * self.lives, 20))
    text(25, str(self.lives), (0, 0, 0), self.x + 48, self.y + 96, align = "center")
    for _ in Bullet._list:
      if collided(self.x, self.y, 96, 96, _.bulletx, _.bullety, _.bulletsize, _.bulletsize):
        self.lives -= Bullet.damage
        Bullet._list.remove(_)
    if self.lives <= 0:
      Spawner._list.pop(self.index_number)
      money += Spawner.reward
    if self.end_time - self.start_time >= Spawner.spawn_time:
      Enemy._list.append(Enemy(self.x + 32, self.y + 32))
      self.start_time = time()
    self.end_time = time()
    screen.blit(self.img, (self.x, self.y))
class Shooter:
  _list = []
  speed = 1
  shoot_time = 3
  reward = 5
  time = 30
  def __init__(self):
    global shooter_img
    self.img = shooter_img
    self.lives = 3
    self.x = random.randint(0, 952)
    self.y = -63
    self.stopx = random.randint(0, 972)
    self.stopy = random.randint(0, 202)
    self.start_time = time()
    self.end_time = time()
    self.index_number = len(Bullet._list) - 1
  def update(self):
    global playerx
    global playery
    global money
    if self.x > self.stopx:
      self.x -= Shooter.speed
    elif self.x < self.stopx:
      self.x += Shooter.speed
    else:
      self.stopx = random.randint(0, 972)
    if self.y > self.stopy:
      self.y -= Shooter.speed
    elif self.y < self.stopy:
      self.y += Shooter.speed
    else:
      self.stopy = random.randint(0, 202)
    pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + 48, 16 * self.lives, 15))
    text(20, str(self.lives), (0, 0, 0), self.x + 24, self.y + 48, align = "center")
    for _ in Bullet._list:
      if collided(self.x, self.y, 48, 48, _.bulletx, _.bullety, _.bulletsize, _.bulletsize):
        self.lives -= Bullet.damage
        Bullet._list.remove(_)
    if self.lives <= 0:
      Shooter._list.pop(self.index_number)
      money += Shooter.reward
    screen.blit(self.img, (self.x, self.y))
    if self.end_time - self.start_time >= Shooter.shoot_time:
      Enemybullet._list.append(Enemybullet(self.index_number))
      self.start_time = time()
    self.end_time = time()
class Tanker:
  def __init__(self):
    pass

class Timer:
  def __init__(self, seconds, running = False):
    self.start_time = time()
    self.end_time = time()
    self.time = seconds
    self.running = running
  def update(self):
    if self.running:
      self.end_time = time()
      if self.end_time - self.start_time >= self.time:
        return True
    return False
  def start(self, seconds = None):
    if seconds != None:
      self.time = seconds
    self.running = True
    self.start_time = time()
    self.end_time = time()
  def stop(self):
    self.running = False
enemy_timer = Timer(Enemy.time, running = True)
spawner_timer = Timer(Spawner.time, running = True)
shooter_timer = Timer(Shooter.time, running = True)
start_time = Timer(fire_speed, running = True)

system("clear")
Spawner._list.append(Spawner())
Enemy._list.append(Enemy())
Shooter._list.append(Shooter())
while game_is_running:
  while status == "playing" and game_is_running:
    mouse_position = pygame.mouse.get_pos()
    mouse_position = list(mouse_position)
    end_time = time()
    enemy_end = time()
    spawner_end = time()
    shooter_end = time()
    mouse_position = pygame.mouse.get_pos()
    mouse_position = list(mouse_position)
    screen.fill((94, 74, 74))
    screen.blit(earth_img, (250, 100))
    screen.blit(money_img, (0, 0))
    text(75, "= $" + str(money), (255, 255, 0), 75, 5)
    screen.blit(miniboss_img, (0, 500))
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_down = True
        if mouse_up == True:
          mouse_clicked = True
          mouse_up = False
      if event.type == pygame.MOUSEBUTTONUP:
        mouse_up = True
        mouse_down = False
    if pressed_keys[pygame.K_LEFT]:
      if playerx > 0:
        playerx -= player_speed
    if pressed_keys[pygame.K_RIGHT]:
      if playerx < 460:
        playerx += player_speed
    if pressed_keys[pygame.K_UP]:
      if playery > 0:
        playery -= player_speed
    if pressed_keys[pygame.K_DOWN]:
      if playery < 460:
        playery += player_speed
    if pressed_keys[pygame.K_SPACE] and start_time.update():
      Bullet._list.append(Bullet())
      start_time.start()
    if enemy_timer.update():
      Enemy._list.append(Enemy())
      enemy_timer.start()
    if spawner_timer.update():
      Spawner._list.append(Spawner())
      spawner_timer.start()
    if shooter_timer.update:
      Shooter._list.append(Shooter())
      shooter_timer.start()
    screen.blit(player, (playerx, playery))
    for _ in Life._list:
      _.update()
    for _ in Bullet._list:
      _.index_number = Bullet._list.index(_)
      _.update()
    for _ in Spawner._list:
      _.index_number = Spawner._list.index(_)
      _.update()
    for _ in Enemy._list:
      _.index_number = Enemy._list.index(_)
      _.update()
    for _ in Shooter._list:
      _.index_number = Shooter._list.index(_)
      _.update()
    for _ in Enemybullet._list:
      _.index_number = Enemybullet._list.index(_)
      _.update()
    if mouse_clicked:
      mouse_clicked = False
    pygame.display.update()
    clock.tick(10)
    if lives <= 0:
      break
for _ in ("YOU LOSE!!!"):
  cprint(_, "red", attrs = ["bold"], end = "")
  stdout.flush()
  sleep(0.1)