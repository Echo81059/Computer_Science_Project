# importing the packages
import numpy as np
import pygame
import random
import time

# Setting dimensions of both the boards and pixels
# Creating and setting time and player variables 
PIXEL_LENGTH = 850
BOARD_LENGTH = 64
scale_ratio = PIXEL_LENGTH/BOARD_LENGTH
t = time.time()
players = []
tail = []

# define food object
# __init__ function operates normally, assgins values to postion and energy
class Food():
    def __init__(self, position: list, energy=1):
        self.position = position
        self.energy = energy

# Creating the Snake Class
# __init__ function operates normally, assigning values to object properties
# change_direction function outputs the value assigned to the parameter dir
# grow function sets grow object property to true
# die function sets 2 global variables.
# Creates an if function that if the global running variable is false the snake "dies" and is removed
# move function is where we create the base for the snakes movements
# We assign values to the snakes direction and if facing that direction, the snake will "move" in this direction
# We accomplish this by adding and removing values from the head and tail, which will eventually look like adding and removing shapes
# If the head reaches the end of the board area - the snkae die function is triggered
# If the head and another part of the tail occupy the same area - the snake die function is triggered
# If the head and food occupies the same area - the snake grow function is triggered, the food is removed, and then food position changes

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
            if abs(self.head[0] - i.position[0]) < 2 and abs(self.head[1] - i.position[1]) < 2:
                self.grow = True
                foods.remove(i)
                foods.append(Food(position=[random.randint(1, BOARD_LENGTH-1), random.randint(1, BOARD_LENGTH-1)]))

# Instantiate the Snake and Food objects
user = Snake(head=[BOARD_LENGTH/2, BOARD_LENGTH/2], snakeID='user')
players.append(user)
foods = []
foods.append(Food(position=[random.randint(1, BOARD_LENGTH-1), random.randint(1, BOARD_LENGTH-1)]))

# update_gui function
def update_gui(players):
    # Creates 2 global variables moved and tail
    global moved
    global tail
    # Fills the screen
    scr.fill((255, 255, 255))
    # Creates the player head
    for player in players:
        pygame.draw.circle(scr, (255, 0, 0), [i*scale_ratio for i in player.head], scale_ratio)
        # Adds more cells values to the snake
        if moved:
            tail = []
            for i in player.tail:
                snake_cell = []
                snake_cell.append((i[0]+player.head[0])*scale_ratio)
                snake_cell.append((i[1]+player.head[1])*scale_ratio)
                tail.insert(0, snake_cell)
        # Drawing the circles
        for i in tail:
            pygame.draw.circle(scr, (30, 255, 50), i, scale_ratio*1.5)
    # Based on the length/number of the foods "eaten" 
    if len(foods) >= 1:
        for food in foods:
            pygame.draw.circle(scr, (255, 0, 0), [i*scale_ratio for i in food.position], scale_ratio*.75)
    moved = False

# Instantiates the board
pygame.init()
scr = pygame.display.set_mode((PIXEL_LENGTH, PIXEL_LENGTH))
running = True
# Creating the controls based on the arrow keys - setting the directions with values
# The while running basically means for these commands to go on the entire time when
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and user.direction != 2:
                user.change_direction(-2)
            if event.key == pygame.K_DOWN and user.direction != 1:
                 user.change_direction(-1)
            if event.key == pygame.K_UP and user.direction != -1:
                 user.change_direction(1)
            if event.key == pygame.K_RIGHT and user.direction != -2:
                 user.change_direction(2)
    # Once the snake spawns in, it is stationary
    # Allows the player to move once the game begins
    if time.time()-t > 0.03:
        t = time.time()
        user.move()
        moved = True
    update_gui(players)
    pygame.display.update()
pygame.quit()
