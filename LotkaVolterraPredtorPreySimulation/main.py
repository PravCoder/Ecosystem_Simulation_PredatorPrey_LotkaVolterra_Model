from time import time
import pygame
import random as rand
from sheep import Sheep
from wolf import Wolf
from constants import *
import matplotlib.pyplot as plt

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("LOTKA-VOLTERRA PREDETOR/PREY MODEL")


def make_grid(rows, width):  # creates empty grid, 0's indicate empty spot
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(0)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows   # gap = distance between each line
    for i in range(rows):  # horizontal lines, (0, 3*gap), (width, 3*gap)
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))  # drawing line(win,color,(x,y),(x,y))
        for j in range(rows):  # vertical lines, (3*gap, 0), (3*gap, width)
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(GREEN)
    for i, row in enumerate(grid):     # grid is made up of lists, for every list-row in grid
        for j, spot in enumerate(row): # for spot-obj in xlist-row
            if spot == 1:
                Sheep(i, j, GAP, ROWS).draw(win)  # calling draw method on spot-obj, draws colors
            if spot == 2:
                Wolf(i, j, GAP, ROWS).draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def initalize_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            grid[i].append(0)

    for i in range(ROWS):
        for j in range(ROWS):
            random_num = rand.random()
            if random_num < initial_occupancy / 2:
                grid[i][j] = 1

            elif random_num > 1 - initial_occupancy:
                grid[i][j] = 2
    return grid


def get_click_pos(pos, rows, width):
    gap = width // rows    # gap = width of cubes
    y, x = pos          # pos = mouse-click-position
    row = y // gap
    col = x // gap
    return row, col  # returns row/col of mouse-click-position

def get_wolf_pop(grid):
    count = 0
    for row in grid:
        for animal in row:
            if animal == 2:
                count += 1
    return count
def get_sheep_pop(grid):
    count = 0
    count = 0
    for row in grid:
        for animal in row:
            if animal == 1:
                count += 1
    return count
def get_grass_pop(grid):
    count = 0
    for row in grid:
        for g in row:
            if g.color == GREEN:
                count += 1
    return count


def get_random_empty_neighbor_pos(grid, i, j):
    neighbors = get_vnn_neighbors(i, j, grid)  # [(i, j), (i,j)], coordinates of 4 neighbors
    empty_neighbors = []

    for n in neighbors:
        if grid[n[0]][n[1]] == 0:
            empty_neighbors.append(n)
    if empty_neighbors != [] and len(empty_neighbors) > 0:
        rand_emp = rand.choice(empty_neighbors)
        return rand_emp
    return None
def get_vnn_neighbors(i, j, grid):  # all 4 neighbors, up,down,left,right. OG-PARAM: i,j
    length = ROWS
    neighbors = []  # equal to [(i,j), (i,j)] the coordinates row/col of all neighbors
    
    neighbors.append([(i+1) % length, j])
    neighbors.append([(i-1 + length) %length, j])
    neighbors.append([i, (j+1)%length])
    neighbors.append([i, (j-1 + length) %length]) 

    """
    if i < length-1 and grid[i + 1][j] != -1:   # down
        neighbors.append((i+1, j))
    if i > 0 and grid[i - 1][j] != -1:    # up
        neighbors.append((i-1, j))
    if j < length-1 and grid[i][j + 1] != -1:   # right
        neighbors.append((i, j+1))
    if j > 0 and grid[i][j - 1] != -1:    # left
        neighbors.append((i, j-1))
    return neighbors  """
    return neighbors


def get_all_neighbors(i, j, grid):  # OG-PARAM: (i,j)
    length = ROWS
    neighbors = []
    """
    for k in range(-1, 1 +1):
        for l in range(-1, 1 +1):
            if k != 0  or l != 0:
                neighbors.append([(i+k+length) %length, (j+l+length) %length])"""
    if i < length-1 and grid[i + 1][j] != -1:   # down
        neighbors.append((i+1, j))
    if i > 0 and grid[i - 1][j] != -1:    # up
        neighbors.append((i-1, j))
    if j < length-1 and grid[i][j + 1] != -1:   # right
        neighbors.append((i, j+1))
    if j > 0 and grid[i][j - 1] != -1:    # left
        neighbors.append((i, j-1))

    if i < length-1 and j < length-1 and grid[i+1][j+1] != -1: # down-right:
        neighbors.append((i+1, j+1))
    if i < length-1 and j > 0 and grid[i+1][j-1] != -1: # down-left:
        neighbors.append((i+1, j-1))
    if i > 0 and j < length-1 and grid[i-1][j+1] != -1: # up-right:
        neighbors.append((i-1, j+1))
    if i > 0 and j > 0 and grid[i-1][j-1]!= -1: # up-left:
        neighbors.append((i-1, j-1))
    
    return neighbors
def get_num_pred_neighbors(grid, i, j):
    count_pred = 0
    neighbors = get_all_neighbors(i, j, grid)

    for neighbor in neighbors:
        if grid[neighbor[0]][neighbor[1]] == 2:
            count_pred += 1;
    return count_pred


def display_model_parameters(s, w):
    print("MODEL PARAMS:")
    print("-----------------------------------")
    print("Sheep Starting Pop: " + str(s))
    print("Wolf Starting Pop: " + str(w))
    print("Sheep Reproduction Rate: " + str(sheep_reproduction_rate ))
    print("Wolf Reproduction Rate: " + str(wolf_reproduction_rate))
    print("Sheep Death Rate: " + str(sheep_death_rate ))
    print("Wolf Death Rate: " + str(wolf_death_rate ))
    print("Predetor-Neighbor-Requirement: "+ str(pred_requirement))
time_values = []
sheep_pop_values = []
wolf_pop_values = []
grass_pop_values = []
"""
OLD-SIMULATION-RULES:
- each species moves randomly and loses energy at each step
- run out of energy dies
- each species capable has probabality of reproduction at each step
- newborn is born in a random empty spot
- if wolf collides with sheep, wolf gains energy sheep dies
- more of an ecology simulation
NEW-SIMULATION-RULES:
- parameters: initals pops, reproduction rates, death rates, predetor-neighbor-threshold requirement
- if sheep is surrounded by a number of wolfs and its probable to reproduce, kill the sheep and reproduce a wolf in that spot
- each as a probablity to die at each step
- each prey has a probalbity to reproduce at each step in a random empty neighbor 
-  they can either live adn stay in teh same spot for the iteration or die, the reproduction and death gives the illusion that they are moving.
- more accurate version of the lotka-volterra model in the spatial domain
PHASE-PLOT:
- x-axis is sheep, y-axis is wolf
- shows the mutal interaction between both species.
- if we imagine a dot the folows the line we can see that the population oscilates. 
"""

def main(win, width):
    ROWS = 50
    grid = initalize_grid()
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
            for i in range(ROWS):
                for j in range(ROWS):
                    if grid[i][j] != 0:
                        if grid[i][j] == 1:
                            num_predators = get_num_pred_neighbors(grid, i, j)
                            if num_predators >= pred_requirement and rand.random() < wolf_reproduction_rate:
                                grid[i][j] = 2
                        if grid[i][j] == 2:
                            if rand.random() < wolf_death_rate:
                                grid[i][j] = 0
                            else:
                                grid[i][j] = 2

            for i in range(ROWS):
                for j in range(ROWS):
                    if grid[i][j] != 0:
                        if grid[i][j] == 1:
                            if rand.random() < sheep_reproduction_rate:
                                neighbor_coords = get_random_empty_neighbor_pos(grid, i, j)
                                if neighbor_coords != None:
                                    grid[neighbor_coords[0]][neighbor_coords[1]] = 1
                            if rand.random() < sheep_death_rate:
                                grid[i][j] = 0
                            else:
                                grid[i][j] = 1
            

        count += 1
        time_values.append(count)
        sheep_pop_values.append(get_sheep_pop(grid))
        wolf_pop_values.append(get_wolf_pop(grid))
        
    pygame.quit()
main(WIN, WIDTH)

print('Sheep: ' + str(sheep_pop_values))
print('Wolf: ' + str(wolf_pop_values))
display_model_parameters(sheep_pop_values[0], wolf_pop_values[0])
plt.plot(time_values, sheep_pop_values, label = "Sheep", color="blue")
plt.plot(time_values, wolf_pop_values, label = "Wolf", color="red")
plt.xlabel('Time')
plt.ylabel('Population of Species')
plt.title('Sheep Wolf Population')
plt.xlim(0, 1500) # og on both is (0, 900)
plt.ylim(0, 1500)
plt.legend()
plt.show()

plt.plot(sheep_pop_values, wolf_pop_values, label = "SheepX WolfY", color="purple")
plt.xlabel('Population of Sheep')
plt.ylabel('Population of Wolf')
plt.title('PHASE PLOT')
plt.xlim(0, 900)
plt.ylim(0, 900)
plt.legend()
plt.show()