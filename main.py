#Importing the packages
import numpy as np
import pygame
import random
import time

#Setting dimensions
PIXEL_LENGTH = 1000
BOARD_LENGTH = 64
scale_ratio = PIXEL_LENGTH/BOARD_LENGTH
t = time.time()
players = []
tail = []

# define food object
class Food():
    def __init__(self, position: list, energy=1):
        self.position = position
        self.energy = energy

# define snake object
class Snake():
    def __init__(self, direction=0, head=[0, 0], tail=[[0, 0]], snakeID=0):
        self.snakeID = snakeID
        if self.snakeID != 'user':
            self.snakeID = len(players)
        self.direction = direction
        self.head = head
        self.tail = tail
        self.grow = False

    def change_direction(self, dir):
        self.direction = dir
        return self.direction

    def grow(self):
        self.grow = True

    def die(self):
        global running
        global players
        if self.snakeID == 'user':
            running = False
            players.remove(user)
        else:
            players.pop(self.snakeID)
    
    def move(self):
        if self.direction == 0: # stationary 
            return
        elif self.grow:
            self.grow = False
        else:
            self.tail.pop(len(self.tail)-1)
        if self.direction == -2: # left
            self.head[0] -= 1
            for i in self.tail:
                i[0] += 1
        if self.direction == 1: # down
            self.head[1] -= 1
            for i in self.tail:
                i[1] += 1
        if self.direction == -1: # up
            self.head[1] += 1
            for i in self.tail:
                i[1] -= 1
        if self.direction == 2: # right
            self.head[0] += 1
            for i in self.tail:
                i[0] -= 1
        self.tail.insert(0, [0, 0])
        if abs(self.head[0]-(BOARD_LENGTH/2)) > BOARD_LENGTH/2 or \
        abs(self.head[1]-(BOARD_LENGTH/2)) > BOARD_LENGTH/2 or [0, 0] in self.tail[1:]:
            self.die()
        for i in foods:
            if abs(self.head[0] - i.position[0]) < 3 and abs(self.head[1] - i.position[1]) < 3:
                self.grow = True
                foods.remove(i)
                foods.append(Food(position=[random.randint(0, BOARD_LENGTH), random.randint(0, BOARD_LENGTH)]))

# Instantiate the Snake and Food objects
user = Snake(head=[BOARD_LENGTH/2, BOARD_LENGTH/2], snakeID='user')
players.append(user)
foods = []
foods.append(Food(position=[random.randint(0, BOARD_LENGTH), random.randint(0, BOARD_LENGTH)]))

def update_gui(players):
    global moved
    global tail
    scr.fill((255, 255, 255))
    for player in players:
        pygame.draw.circle(scr, (255, 0, 0), [i*scale_ratio for i in player.head], scale_ratio)
        if moved:
            tail = []
            for i in player.tail:
                snake_cell = []
                snake_cell.append((i[0]+player.head[0])*scale_ratio)
                snake_cell.append((i[1]+player.head[1])*scale_ratio)
                tail.insert(0, snake_cell)
        for i in tail:
            pygame.draw.circle(scr, (255, 0, 0), i, scale_ratio)
    if len(foods) >= 1:
        print(foods)
        for food in foods:
            pygame.draw.circle(scr, (80, 80, 80), [i*scale_ratio for i in food.position], scale_ratio/2)
    moved = False

pygame.init()
scr = pygame.display.set_mode((PIXEL_LENGTH, PIXEL_LENGTH))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                user.change_direction(-2)
            if event.key == pygame.K_DOWN:
                 user.change_direction(-1)
            if event.key == pygame.K_UP:
                 user.change_direction(1)
            if event.key == pygame.K_RIGHT:
                 user.change_direction(2)
    if time.time()-t > 0.05:
        t = time.time()
        user.move()
        moved = True
    update_gui(players)
    pygame.display.update()
pygame.quit()
