# importing the packages
import numpy as np
import pygame
import random
import time

visu = True

#Setting dimensions
PIXEL_LENGTH = 850
BOARD_LENGTH = 64
scale_ratio = PIXEL_LENGTH/BOARD_LENGTH
t = time.time()
players = []

# define food object
class Food():
    def __init__(self, position: list, energy=1):
        self.position = position
        self.energy = energy
    
    def respawn(self, board_length):
        self.position = [random.randint(1, board_length-1), random.randint(1, board_length-1)]

# define snake object
class Snake():
    def __init__(self, snakeID, direction=0, head=[0, 0], tail=[[0, 0]], ):
        self.snakeID = snakeID
        self.direction = direction
        self.head = head
        self.tail = tail
        self.reward = 0
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

class SnakeEnv():
    def __init__(self, board_length):
        self.board_length = board_length
        self.player = Snake(head=[board_length/2, board_length/2], snakeID='user')
        self.food = Food(position=[random.randint(1, board_length-1), random.randint(1, board_length-1)])

    def step(self):
        self.player.move()
        if abs(self.player.head[0] - self.food.position[0]) < 2 and abs(self.player.head[1] - self.food.position[1]) < 2:
            self.player.grow = True
            self.food.respawn(self.board_length)
        state = [self.food.position, self.player.direction, self.player.head, self.player.tail]
        return self.player.reward, state 

# Instantiate the environment 
env = SnakeEnv(BOARD_LENGTH)

def update_gui(state):
    scr.fill((255, 255, 255))
    food_pos = state[0]
    player_head = state[2]
    player_tail = state[3]
    pygame.draw.circle(scr, (255, 0, 0), [i*scale_ratio for i in player_head], scale_ratio)
    scaled_tail = []
    for i in player_tail:
        snake_cell = []
        snake_cell.append((i[0]+player_head[0])*scale_ratio)
        snake_cell.append((i[1]+player_head[1])*scale_ratio)
        scaled_tail.insert(0, snake_cell)
    for i in scaled_tail:
        pygame.draw.circle(scr, (30, 255, 50), i, scale_ratio*1.5)
    pygame.draw.circle(scr, (255, 0, 0), [i*scale_ratio for i in food_pos], scale_ratio*.75)

pygame.init()
scr = pygame.display.set_mode((PIXEL_LENGTH, PIXEL_LENGTH))
running = True
if visu:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and env.player.direction != 2:
                    env.player.change_direction(-2)
                if event.key == pygame.K_DOWN and env.player.direction != 1:
                    env.player.change_direction(-1)
                if event.key == pygame.K_UP and env.player.direction != -1:
                    env.player.change_direction(1)
                if event.key == pygame.K_RIGHT and env.player.direction != -2:
                    env.player.change_direction(2)
        if time.time()-t > 0.03: # delay speed in between each step (in addition to ~0.016 sec delay inflicated by pygame.display.update method)
            t = time.time()
            reward, state = env.step()
            update_gui(state)
        pygame.display.update()
    pygame.quit()
else:
    pass
