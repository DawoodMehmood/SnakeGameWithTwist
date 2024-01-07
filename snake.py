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


def message_to_display(msg, color, y_displace=0, size="small"):
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



def fruit(snake_list, obstacle_free_list, boundary=True, obstacle=True):
    """Function deals with the placement of the fruit on the screen"""
    # Total width -30 to keep the complete fruit within the screen:(30 is width and length of fruit)
    def fruit_check():
        """Generates 'x' and 'y' coordinates of fruit for 3 situations(levels)"""
        if boundary and not obstacle:  # Fruit cannot appear on boundary
            fruit_x = random.randrange(box, x_length - box, 30)
            fruit_y = random.randrange(box, y_length - box, 30)
        if not boundary and not obstacle:  # Fruit can appear anywhere
            fruit_x = random.randrange(0, x_length - box, 30)
            fruit_y = random.randrange(0, y_length - box, 30)
        if boundary and obstacle:  # Fruit can not appear on boundary and obstacle
            # Coordinates for fruit selected from an obstacle free list
            fruit_x, fruit_y = random.choice(obstacle_free_list)
        return fruit_x, fruit_y
    fruit_x, fruit_y = fruit_check()
    # fruit coordinates are generated until they are not equal to snake coordinates
    while (fruit_x, fruit_y) in snake_list:
        fruit_x, fruit_y = fruit_check()
    return fruit_x, fruit_y

def direction(direct, x_coordinate, y_coordinate,  distance=30):       # Distance =width(or length)of box of grid-30
    """Function to enable automatic movement of snake,variable 'direct' is used to store which direction
     the snake moves in automatically,parameter distance refers to the distance snake travels in one iteration
     and returns the coordinates of snake('x' and 'y' coordinate) as a result of an event"""
    if direct == "UP":
        y_coordinate -= distance
    if direct == "DOWN":
        y_coordinate += distance
    if direct == "RIGHT":
        x_coordinate += distance
    if direct == "LEFT":
        x_coordinate -= distance
    return x_coordinate, y_coordinate 



def leaves_screen(x_coordinate, y_coordinate):
    """Function to deal with snake if it leaves screen,if its coordinates are beyond the grid, it is sent
     at opposite side of where it left.Like if it left screen at RIGHT MOST (599, 0) it is sent to LEFT MOST (0,0).
     It returns new coordinates of snake('x' and 'y' coordinate)"""

    if y_coordinate >= y_length - 1:
        y_coordinate = 0
    elif y_coordinate <= -1:
        y_coordinate = y_length - box
    if x_coordinate <= -1:
        x_coordinate = x_length - box
    elif x_coordinate >= x_length - 1:
        x_coordinate = 0
    return x_coordinate, y_coordinate

def score(data):
    """Function to count score of the user and displaying on screen"""
    score = small_font.render("Score: "+str(data), True, WHITE)
    screen.blit(score, [270, 0])



def dis_screen():
    """Function to display menu at start-up and initializes"""

    pygame.mixer.Sound.play(menu)     # Playing the music for menu
    show_the_welcome_screen = True
    while show_the_welcome_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.mixer.Sound.stop(menu)     # Stop playing the music for the new event
                    # Declaring credentials as per level selection
                    boundary = False
                    obstacle = False
                    colour = SKIN1
                    return boundary, obstacle, colour
                if event.key == pygame.K_m:
                    pygame.mixer.Sound.stop(menu)     # Stop playing the music for the new event
                    # Declaring credentials as per level selection
                    boundary = True
                    obstacle = False
                    colour = SKIN2
                    return boundary, obstacle, colour
                if event.key == pygame.K_h:
                    pygame.mixer.Sound.stop(menu)     # Stop playing the music for the new event
                    # Declaring credentials as per level selection
                    boundary = True
                    obstacle = True
                    colour = SKIN3
                    return boundary, obstacle, colour
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        # All the text to display on the screen
        message_to_display("Snake Frenzy", RED, -120, "medium")
        message_to_display("The objective of this game is to eat fruits", BLUE, -60)
        message_to_display("The more fruit you eat, the longer you get", BLUE, -30)
        message_to_display("If you run into yourself you die!", BLUE, 0)
        message_to_display("Press [E] for Easy Level", BLACK, 120)
        message_to_display("Press [M] for Medium Level", BLACK, 150)
        message_to_display("Press [H] for Hard Level", BLACK, 180)
        message_to_display("Press [Q] to Quit", BLACK, 210)

        pygame.display.update()
        clock.tick(15)


def gameover():
    """Function for the displaying of menu when game gets over by a condition in main loop.
    It also calls the respective levels if player wants to play more"""
    pygame.mixer.music.stop()     # Stop playing the sound of menu
    pygame.mixer.Sound.play(gameovr)      # Playing the music for gameover
    show_the_welcome_screen = True      # Showing the welcome screen

    while show_the_welcome_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.mixer.Sound.stop(gameovr)     # Stop playing the music for the new event
                    game(snake, head, boundary=False, obstacle=False, colour=SKIN1)
                    pygame.mixer.music.stop()  # Stop playing the sound of menu
                    pygame.mixer.Sound.play(gameovr)  # Playing the music for gameover
                    pygame.mixer.music.stop()
                if event.key == pygame.K_m:
                    pygame.mixer.Sound.stop(gameovr)     # Stop playing the sound of gameover
                    game(snake, head, boundary=True, obstacle=False, colour=SKIN2)
                    pygame.mixer.music.stop()  # Stop playing the sound of menu
                    pygame.mixer.Sound.play(gameovr)  # Playing the music for gameover

                if event.key == pygame.K_h:
                    pygame.mixer.Sound.stop(gameovr)     # Stop playing the sound of gameover
                    game(snake, head, boundary=True, obstacle=True, colour=SKIN3)
                    pygame.mixer.music.stop()  # Stop playing the sound of menu
                    pygame.mixer.Sound.play(gameovr)  # Playing the music for gameover
          
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        # All the text to display on the screen
        message_to_display("Game Over!!!", RED, -90, "medium")
        message_to_display(f"Score: {total_points}", BLUE, 0)
        message_to_display("Press [E] for Easy Level", BLACK, 120)
        message_to_display("Press [M] for Medium Level", BLACK, 150)
        message_to_display("Press [H] for Hard Level", BLACK, 180)
        message_to_display("Press [Q] to Quit", BLACK, 210)
        # File handling for storing and display of highscore by comparing with the points scored
        # If the file to store highscore does not exist, it is created with highscore 0
        if not isfile("Highscore.txt"):
            with open("Highscore.txt", 'w') as file:
                file.write("0")
        with open("Highscore.txt") as file:
            data = file.read()
        if eval(data) < total_points:
            file = open("Highscore.txt", "w")
            file.write(str(total_points))
            file.close()
        else:
            message_to_display(f"High Score: {data}", BLUE, 30)
        pygame.display.update()
        clock.tick(15)

