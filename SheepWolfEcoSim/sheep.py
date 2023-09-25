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

    def draw(self, win):
        win.blit(SHEEP_IMG, (self.x, self.y))
        #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  # this method is called on spot-obj

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