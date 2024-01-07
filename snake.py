# Importing the modules
import pygame
import random
import time
from os.path import isfile

# Initializing the 'pygame' module
pygame.init()
            # Game Specific Variables #

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Setting up a standard dimension for the grid
box = 30

# Setting up the main display screen
x_length = 600      # Horizontal length of grid
y_length = 600      # Vertical length of grid
screen_size = (x_length, y_length)      # Size of screen saved in a tuple
screen = pygame.display.set_mode(screen_size)    # Prints grid

# Setting up the font size and style
small_font = pygame.font.SysFont("comicsansms", 20)
medium_font = pygame.font.SysFont("comicsansms", 40)

# Background for start menu and game over menu
background = pygame.image.load('pictures/bg.jpg')
background = pygame.transform.scale(background, (x_length, y_length)).convert_alpha()

# Simple fruit image
fruimg = pygame.image.load('pictures/apple.png')
fruimg = pygame.transform.scale(fruimg, (box, box)).convert_alpha()

# Images for special fruits
fruimg2 = pygame.image.load('pictures/wm.png')
fruimg2 = pygame.transform.scale(fruimg2, (box, box)).convert_alpha()

fruimg3 = pygame.image.load('pictures/wm1.png')
fruimg3 = pygame.transform.scale(fruimg3, (box, box)).convert_alpha()

fruimg4 = pygame.image.load('pictures/wm2.png')
fruimg4 = pygame.transform.scale(fruimg4, (box, box)).convert_alpha()

# Sounds for different aspects
fruit_sound = pygame.mixer.Sound('sounds/Plop.ogg')
gameovr = pygame.mixer.Sound('sounds/gameover.ogg')
menu = pygame.mixer.Sound('sounds/menu.mp3')

# Defining colours using RGB Codes
RED   = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
SKIN1 = (173, 119, 75)
SKIN2 = (100, 100, 100)
SKIN3 = (150, 141, 200)

# Setting the window title
pygame.display.set_caption("Snake Frenzy by Coding Aztecs")

# Defining initial position of the snake
x_coordinate = 120      # X coordinate of snake's head
y_coordinate = 30       # Y coordinate of snake's head

# The head of the snake is stored in a separate list and then added to the main list snake
# This makes it easier to manipulate the snake as all corresponding actions are concerned with snake's head
head = [x_coordinate, y_coordinate]

# A list of lists is used to store coordinates of body part of snake
# The 0 index represents head, all subsequent index other parts
snake = [[head[0] - box, head[1]], [head[0] - box*2, head[1]], [head[0] - box*3, head[1]]]

                                    # Functioning #

# Taking the coordinates of whole grid(self-made) in a list
grid = list()
for x in range(0, 600, 30):
    for y in range(0, 600, 30):
        grid.append((x, y))

# Taking the coordinates of the obstacle(for hard level)
obstacle_coordinates = list()
for coordinate in range(210, 390, 30):
    obstacle_coordinates.append((coordinate, 270))
    obstacle_coordinates.append((coordinate, 300))
for coordinate in range(0, 600, 30):
    obstacle_coordinates.append((coordinate, 0))
    obstacle_coordinates.append((0, coordinate))
    obstacle_coordinates.append((570, coordinate))
    obstacle_coordinates.append((coordinate, 570))
obstacle_coordinates = list(set(obstacle_coordinates))
for i in obstacle_coordinates:
    grid.remove(i)      # Removing obstacle(coordinates) from grid so fruit should not appear on obstacle

    """Function to print message on game display and takes the text,color and position along y-axis as arguments"""
    def text_object(msg, color, size):
        """Function deals with the formatting of the text to be written,takes in the text and color as arguments"""
        # textSurface = font.render(msg, True, color)
        # return textSurface, textSurface.get_rect()
        if size == "small":
            textSurface = small_font.render(msg, True, color)
            return textSurface, textSurface.get_rect()

        if size == "medium":
            textSurface = medium_font.render(msg, True, color)
            return textSurface, textSurface.get_rect()

    textSurf, textRect = text_object(msg, color, size)
    textRect.center = (x_length/2), (y_length/2) + y_displace
    screen.blit(textSurf, textRect)

