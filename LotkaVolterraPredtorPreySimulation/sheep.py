import pygame
from constants import *
import random as rand

class Sheep:  # gap = Totalwidth // rows. width = gap
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width  
        self.y = row * width
        self.alive = False
        self.energy = 1000
        self.reproduction_percentage = sheep_reproduction_rate
        self.neighbors = []
        self.width = width
        self.total_rows = 50
        self.color = WHITE  
        self.type = "sheep"

    def update_neighbors(self, grid):     # method is called on every spot-obj, uses its attributes
        self.neighbors = []   # add spot-obj to self.neighbors if neighbor is blank
        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].type != "":   # down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].type != "":    # up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows-1 and not grid[self.row][self.col + 1].type != "":   # right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].type != "":    # left
            self.neighbors.append(grid[self.row][self.col - 1])
        return self.neighbors

    def get_num_pred_neighbors(self, grid):
        count = 0
        spots = self.update_neighbors(grid)
        for s in spots:
            if s.type =="wolf":
                count += 1
        return count

    def draw(self, win):
        win.blit(SHEEP_IMG, (self.x, self.y))

    def move_random(self):
        valid = ["S"]
        if self.row+1 < self.total_rows:
            valid.append("D")
        if self.row-1 >= 0:
            valid.append("U")
        if self.col+1 < self.total_rows:
            valid.append("R")
        if self.col-1 >= 0:
            valid.append("L")
        
        move = rand.choice(valid)
        if move == "U":
            self.row = self.row - 1
            self.update_position()
            self.energy -= 35
        if move == "D":
            self.row = self.row + 1
            self.update_position()
            self.energy -= 35
        if move == "R":
            self.col = self.col + 1
            self.update_position()
            self.energy -= 35
        if move == "L":
            self.col = self.col - 1
            self.update_position()
            self.energy -= 35
        if move == "S":
            return

    def update_position(self):
        self.x = self.col * self.width 
        self.y = self.row * self.width 

    def reproduce(self):
        if rand.randint(0,100) <= (self.reproduction_percentage*100):
            return True