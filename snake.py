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


def game(snake, head, boundary, obstacle, colour):
    """This function can be considered as the core function of the game like main loop.
     It control all the contents for different levels from appearance to execution.It takes in
      the snake,head,boundary,obstacle and color for the snakes of different levels"""
    # Initialising the snake
    head = [x_coordinate, y_coordinate]  # Placing the head
    # Placing the rest of the snake
    snake = [[head[0] - box, head[1]], [head[0] - box * 2, head[1]], [head[0] - box * 3, head[1]]]

    # checking the level selection by the user and loading relevant image
    if not boundary and not obstacle:       # Easy level
        bgimg = pygame.image.load('pictures/bck1.png')   # Background image for easy level
        bgimg = pygame.transform.scale(bgimg, (x_length, y_length)).convert_alpha()

    if boundary and not obstacle:       # Medium level
        bgimg = pygame.image.load('pictures/bck2.png')   # background image for medium level
        bgimg = pygame.transform.scale(bgimg, (x_length, y_length)).convert_alpha()

    if boundary and obstacle:       # Hard level
        bgimg = pygame.image.load('pictures/bck3.png')       # Background image for hard level
        bgimg = pygame.transform.scale(bgimg, (x_length, y_length)).convert_alpha()

    global total_points
    total_points = 0      # Initializing the score to Zero
    normal_points = 0      # Initializing secondary score(count of normal fruit eaten) to Zero
    pygame.mixer.music.load('sounds/main_game.wav') # playing sound for gameplay
    pygame.mixer.music.play(-1)
    normal_fruit_x, normal_fruit_y = fruit(snake, grid, boundary, obstacle)      # For normal fruit
    bonus_fruit_x, bonus_fruit_y = fruit(snake, grid, boundary, obstacle)  # For bonus score fruit
    bad_fruit_x, bad_fruit_y = fruit(snake, grid, boundary, obstacle)  # For fruit that increase length
    good_fruit_x, good_fruit_y = fruit(snake, grid, boundary, obstacle)  # For fruit that decrease length

    # To make sure fruits don't appear on each other
    while bonus_fruit_x == normal_fruit_x and bonus_fruit_y == normal_fruit_y:
        bonus_fruit_x, bonus_fruit_y = fruit(snake, grid, boundary, obstacle)

    while (bad_fruit_x == normal_fruit_x and bad_fruit_y == normal_fruit_y) or (bad_fruit_x == good_fruit_x and bad_fruit_y == good_fruit_y):
        bad_fruit_x, bad_fruit_y = fruit(snake, grid, boundary, obstacle)

    while (good_fruit_x == normal_fruit_x and good_fruit_y == normal_fruit_y) or (good_fruit_x == bad_fruit_x and good_fruit_y == bad_fruit_y):
        good_fruit_x, good_fruit_y = fruit(snake, grid, boundary, obstacle)

    direct = "RIGHT"     # Declaring the initial direction of snake
    speed = 30      # The spaces(30) snake travels in a single loop-as per dimensions of box of grid
    quit_game = False       # When quit_game is True, main loop breaks and game ends
    time_delay = 0.12   # Sets time after which screen updates - currently set to 120 ms - used for controlling speed
    current_time = 0        # Initializing the time for taking difference for timer
    bonus_fruit_time = 0        # Initializing the time for taking difference for timer
    good_bad_fruit_time = 0        # Initializing the time for taking difference for timer
    while quit_game == False:
        for event in pygame.event.get():        # Condition to quit game if window is closed
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:    # Conditions to move snake according to user input
                # Following are method to deal with input of user
                # If user presses arrow keys, change direction
                # 180 degree change of snake prohibited by checking initial direction
                # break is used so that only one change of direction command is executed in one iteration
                if event.key == pygame.K_DOWN:
                    if direct == "UP":
                        continue
                    direct = "DOWN"
                    break
                if event.key == pygame.K_UP:
                    if direct == "DOWN":
                        continue
                    direct = "UP"
                    break
                if event.key == pygame.K_RIGHT:
                    if direct == "LEFT":
                        continue
                    direct = "RIGHT"
                    break
                if event.key == pygame.K_LEFT:
                    if direct == "RIGHT":
                        continue
                    direct = "LEFT"
                    break

        for body in range(len(snake) - 1, 0, -1):
            snake[body] = snake[body-1]
        snake[0] = head
        head = direction(direct, head[0], head[1], speed)  # Checking the direction in result of an event

        if not boundary and not obstacle:
            head = leaves_screen(head[0], head[1])  # Checking leaving of screen by snake for easy level
        if boundary:        # Checking collision with boundary by snake for medium level
            if head[0] < 30 or head[0] > 569 or head[1] < 30 or head[1] > 569:
                quit_game = True
            if obstacle:        # Checking collision with obstacle by snake for hard level
                if (209 < head[0] < 390) and (269 < head[1] < 330):
                    quit_game = True

        if head == (normal_fruit_x, normal_fruit_y):      # Checking collision with fruit for another to appear
            normal_fruit_x, normal_fruit_y = fruit(snake, grid, boundary, obstacle)
            snake.append([])        # Increment in snake's length += 1
            pygame.mixer.Sound.play(fruit_sound)
            total_points += 1            # Increment in score
            normal_points += 1
            if time_delay > 0.05:        # Controls the speed of the game
                time_delay -= 0.003
            # Checking if score is multiple of 5 for special fruit appearance
            if normal_points % 5 == 0 and normal_points != 0:
                if normal_points % 10 == 0:      # Checking if score is multiple of 10 for special fruit appearance
                    good_bad_fruit_time = pygame.time.get_ticks()
                    bad_fruit_x, bad_fruit_y = fruit(snake, grid, boundary, obstacle)
                    good_fruit_x, good_fruit_y = fruit(snake, grid, boundary, obstacle)
                else:
                    bonus_fruit_time = pygame.time.get_ticks()
                    bonus_fruit_x, bonus_fruit_y = fruit(snake, grid, boundary, obstacle)

        # Checking if score is multiple of 5 for special fruit appearance
        if normal_points % 5 == 0 and normal_points != 0:
            if normal_points % 10 == 0:      # Checking if score is multiple of 10 for special fruit appearance
                # display image for special fruits after eating 10 ordinary fruits
                screen.blit(fruimg3, (good_fruit_x, good_fruit_y, box, box))
                screen.blit(fruimg4, (bad_fruit_x, bad_fruit_y, box, box))
                if head[0] == good_fruit_x and head[1] == good_fruit_y:    # Checking collision with fruit
                    good_fruit_x, good_fruit_y = fruit(snake, grid, boundary, obstacle)
                    pygame.mixer.Sound.play(fruit_sound) # play sound when snake eats fruit
                    del snake[-5:-1]   # Remove 4 blocks from snake list
                    normal_points = 0         # Returning normal fruit count to initial state
                elif head[0] == bad_fruit_x and head[1] == bad_fruit_y:     # Checking collision with fruit
                    bad_fruit_x, bad_fruit_y = fruit(snake, grid, boundary, obstacle)
                    pygame.mixer.Sound.play(fruit_sound) # play sound when snake eats fruit
                    snake.extend([[], [], [], []])  # Adding 4 blocks to snake list
                    normal_points = 0         # Returning normal fruit count to initial state
                if current_time - good_bad_fruit_time > 3000:  # Fruit appears for 3 seconds
                    good_fruit_x, good_fruit_y = -30, -30
                    bad_fruit_x, bad_fruit_y = -30, -30
            else:
                screen.blit(fruimg2, (bonus_fruit_x, bonus_fruit_y)) # display image for special fruit after eating 5 ordinary fruits
                if head[0] == bonus_fruit_x and head[1] == bonus_fruit_y:
                    bonus_fruit_x, bonus_fruit_y = fruit(snake, grid, boundary, obstacle)
                    pygame.mixer.Sound.play(fruit_sound) # play sound when snake eats fruit
                    total_points += 3     # Increment 3 in score
                if current_time - bonus_fruit_time > 3000:  # Fruit appears for 3 second
                    bonus_fruit_x, bonus_fruit_y = -30, -30

        # Used to check collision of snake's head with its body
        if head in snake:
            quit_game = True
            
        # LOOP USED TO PRINT every part of snake on screen
        count = 0
        for body in snake:
            if len(body) == 0:
                continue
            # If count == 0, the first part head is printed and a different colour is used for it
            if count == 0:
                pygame.draw.rect(screen, BLACK, [body[0], body[1], box, box])
                count += 1
                continue
            pygame.draw.rect(screen, colour, [body[0], body[1], box, box])
            count += 1

        pygame.display.flip()  # UPDATE SCREEN
        clock.tick(60)  # Set fps to 60

        # PRINTING ON SCREEN
        screen.fill(WHITE)  # Clear screen so new images can be shown
        screen.blit(bgimg, (0, 0)) # displaying background image

        # Fruit appears at random position(width and length = 30)
        
        screen.blit(fruimg, (normal_fruit_x, normal_fruit_y, box, box)) # displaying ordinary fruits
        score(total_points)       # Calling the function to show score on screen
        current_time = pygame.time.get_ticks()
        time.sleep(time_delay)  # Used to manage delay between successive iterations
        # time_delay decreases everytime fruit is eaten so the loop runs more often and snake is faster


# To start until user press Q to exit or click cross on window.
boundary, obstacle, colour = dis_screen()
game(snake, head, boundary, obstacle, colour)
gameover()


