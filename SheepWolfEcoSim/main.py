from time import time
import pygame
import random as rand
from queue import PriorityQueue
from sheep import Sheep
from wolf import Wolf
from constants import *
import matplotlib.pyplot as plt

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SHEEP WOLF GRASS SIMULATION")

sheepies = []
wolfies = []

class Grass: 
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  
        self.y = col * width
        self.color = GREEN 
        self.alive = False
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.energy = 100
        self.regrowth_rate = 0.01

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  # this method is called on spot-obj

    def update_neighbors(self, grid):    
        self.neighbors = []   # add spot-obj to self.neighbors if neighbor is blank
        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].alive == True:   # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].alive == True:   # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col + 1].alive == True:   # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].alive == True:   # left
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []               # grid is made of lists with spot-objects
    gap = width // rows     # gap = width of cube
    for i in range(rows):   # for every row  
        grid.append([])    # append empty list-row to grid
        for j in range(rows):  # for every spot in empty list-row
            spot = Grass(i, j, gap, rows)   # spot-obj, passing(row, col, width, total_rows)
            grid[i].append(spot)         # append spot-obj to list-row i in grid
    return grid

def make_sheep_grid(rows, width):
    gap = width // rows  
    for i in range(ROWS): 
        sheepies.append([])   
    
    for j in range(inital_sheep_pop):
        avalible = get_avalible()
        random_row = rand.choice(list(avalible.keys())) # indx
        random_col = rand.choice(avalible[random_row])

        s = Sheep(random_row, random_col, gap, rows)   
        sheepies[random_row].append(s) 
    return sheepies

def make_wolf_grid(rows, width):
    gap = width // rows  
    for i in range(ROWS): 
        wolfies.append([])   
    
    for j in range(inital_wolf_pop):
        avalible = get_avalible()
        random_row = rand.choice(list(avalible.keys())) # indx
        random_col = rand.choice(avalible[random_row])

        s = Wolf(random_row, random_col, gap, rows)   
        wolfies[random_row].append(s) 
    return wolfies

def get_avalible():  # in sheepies
    row_col = {}  # {row-indx: [avalible, cols, indx]}
    for i, row in enumerate(sheepies):
        if len(row) < ROWS:   # has empty spots
            not_avalible_cols = []
            for sheep in row:
                not_avalible_cols.append(sheep.col)
            available_cols = []
            for c in range(ROWS):
                if c not in not_avalible_cols:
                    available_cols.append(c)
            row_col[i] = available_cols 
    return row_col


def draw_grid(win, rows, width):
    gap = width // rows   # gap = distance between each line
    for i in range(rows):  # horizontal lines, (0, 3*gap), (width, 3*gap)
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))  # drawing line(win,color,(x,y),(x,y))
        for j in range(rows):  # vertical lines, (3*gap, 0), (3*gap, width)
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(GREEN)
    for row in grid:     # grid is made up of lists, for every list-row in grid
        for spot in row: # for spot-obj in xlist-row
            spot.draw(win)  # calling draw method on spot-obj, draws colors

    for row in sheepies:     # grid is made up of lists, for every list-row in grid
        for animal in row: # for spot-obj in list-row
            animal.draw(win)  # calling draw method on spot-obj, draws colors
    for row in wolfies:     # grid is made up of lists, for every list-row in grid
        for wolf in row: # for spot-obj in list-row
            wolf.draw(win)  # calling draw method on spot-obj, draws colors

    draw_grid(win, rows, width)
    pygame.display.update()

def get_click_pos(pos, rows, width):
    gap = width // rows    # gap = width of cubes
    y, x = pos          # pos = mouse-click-position

    row = y // gap
    col = x // gap
    
    return row, col  # returns row/col of mouse-click-position

def get_wolf_pop():
    count = 0
    for row in wolfies:
        count += len(row)
    return count
def get_sheep_pop():
    count = 0
    for row in sheepies:
        count += len(row)
    return count
def get_grass_pop(grid):
    count = 0
    for row in grid:
        for g in row:
            if g.color == GREEN:
                count += 1

    return count

def display_model_parameters():
    print("MODEL PARAMS:")
    print("-----------------------------------")
    print("Sheep Starting Pop: " + str(inital_sheep_pop))
    print("Wolf Starting Pop: " + str(inital_wolf_pop))
    print("Sheep Reproduction Rate: " + str(sheep_reproduction_rate ))
    print("Wolf Reproduction Rate: " + str(wolf_reproduction_rate))
    print("Sheep Death Rate: " + str(sheep_death_rate ))
    print("Wolf Death Rate: " + str(wolf_death_rate ))

time_values = []
sheep_pop_values = []
wolf_pop_values = []
grass_pop_values = []

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)  # returns grid
    sheepies = make_sheep_grid(ROWS, width)
    wolfies = make_wolf_grid(ROWS, width)

    run = True
    started = False

    clock = pygame.time.Clock()
    count = 0
    while run:
        clock.tick(FPS)
        draw(win, grid, ROWS, width)      # calling draw function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True

        if started == True:
            for i, row in enumerate(wolfies):  # MOVE WOLFS
                for w in row:
                    if w.energy <= 0:
                        wolfies[i].remove(w)
                    else:
                        w.move_random()  # wolf population stagnite at 1000
                        if w.reproduce() == True  and rand.randint(0,100) <= 50:
                            wolfies[i].append(Wolf(rand.randint(0, ROWS), rand.randint(0, ROWS), GAP, ROWS))

            for i, row in enumerate(sheepies): # CHECK WOLF-SHEEP COLLISION
                for s in row:
                    for rowW in wolfies:
                        for w in rowW:
                            if s.row == w.row and s.col == w.col:
                                if s in sheepies[i]:
                                    sheepies[i].remove(s)
                                    w.energy += 300

                                    # delete below line it reproduces wolf for evry time it eats wolf
                                    #wolfies[i].append(Wolf(rand.randint(0, ROWS), rand.randint(0, ROWS), GAP, ROWS))
            
            for i, row in enumerate(sheepies):  # MOVE SHEEPS
                for s in row:
                    if s.energy <= 0:
                        sheepies[i].remove(s)
                    else:  # CHANGE PREDOUCTION ROW/COL BACK TO PARENT
                        s.move_random()              # change sheep reproduction conditions
                        if s.reproduce() == True and rand.randint(0,100) <= 50:
                            sheepies[i].append(Sheep(rand.randint(0, ROWS), rand.randint(0, ROWS), GAP, ROWS))
                        
 
              # uncomment this line to give sheep infite grass

            for rowW in sheepies:
                for s in rowW:
                    
                    s.energy += 10 

        count += 1
        time_values.append(count)
        sheep_pop_values.append(get_sheep_pop())
        wolf_pop_values.append(get_wolf_pop())
        grass_pop_values.append(get_grass_pop(grid))
        
    pygame.quit()
main(WIN, WIDTH)


display_model_parameters()
# plotting the line 1 points 
plt.plot(time_values, sheep_pop_values, label = "Sheep", color="blue")
plt.plot(time_values, wolf_pop_values, label = "Wolf", color="red")
plt.plot(time_values, grass_pop_values, label = "Grass", color="green")
# naming the x axis
plt.xlabel('Time')
# naming the y axis
plt.ylabel('Population of Species')
# giving a title to my graph
plt.title('Sheep Wolf Population')
  
plt.xlim(0, 2000)
plt.ylim(0, 1500)

# show a legend on the plot
plt.legend()
# function to show the plot
plt.show()