import pygame
import os
RED = (255, 0, 0)
GREEN = (102,205,0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BROWN = (139,101,8)

WIDTH = 800
GAP = WIDTH//50
FPS = 60
ROWS = 50

SHEEP_SURFACE = pygame.image.load(os.path.join("LotkaVolterraPredtorPreySimulation/images", "s2.jpg"))  # bg_surface
SHEEP_IMG = pygame.transform.scale(SHEEP_SURFACE, (16, 20))
inital_sheep_pop = 100
inital_wolf_pop = 50

sheep_reproduction_rate = 0.4  # S-0.06, W-0.03
wolf_reproduction_rate = 0.8

sheep_death_rate = 0.2  # delete this functionaltity to get original.
wolf_death_rate = 0.1

pred_requirement = 2
initial_occupancy = 0.06


"""
VERSION 1: with death rates
sheep_reproduction_rate = 0.06  # S-0.06, W-0.03
wolf_reproduction_rate = 0.03

sheep_death_rate = 0.003  # delete this functionaltity to get original.
wolf_death_rate = 0.006

"""

"""
VERSION 2: no death rates
sheep_reproduction_rate = 0.06  # S-0.06, W-0.03
wolf_reproduction_rate = 0.03


"""

"""
VERSION 3L: WITH DEATH
inital_sheep_pop = 100
inital_wolf_pop = 50

sheep_reproduction_rate = 0.06  # S-0.06, W-0.03
wolf_reproduction_rate = 0.03

sheep_death_rate = 0.003  # delete this functionaltity to get original.
wolf_death_rate = 0.006
"""