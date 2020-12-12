# Author: Nicholas Meyer, nmeyer2018@my.fit.edu
# Course: CSE 2050, Fall 2020
# Project: Save The Manatee (GUI)
"""Uses pygame to run game where the goal is to guide the manatee to safety."""
from sys import stdout, exit
from argparse import ArgumentParser
from urllib import request
import pygame


def create_board(lines, board, boats, hyacinths, grasses, coquinas, water):
    # This function adds each line of the input
    # file to the 2D array "board" and runs the
    # functions to create boat, hyacinth, seagrass
    # coquina, and water arrays.
    for line in lines:
        line = line.decode()
        cur_line = []
        for i in range(0, len(line) - 1):
            cur_line.append(line[i])
        board.append(cur_line)

    create_array(board, boats, '*')
    create_array(board, hyacinths, '\\')
    create_array(board, grasses, '.')
    create_array(board, coquinas, '#')
    create_array(board, water, ' ')


def create_array(game_board, array, char):
    # Creates an array of coordinates for a
    # specific character in the game board.
    for i in range(0, len(game_board)):
        for j in range(0, len(game_board[i])):
            if game_board[i][j] == char:
                array.append((i, j))


def move_boat_across(boat_coord, side):
    # This function checks if a boat can be moved
    # either left or right and if so, performs
    # the action. If it can, the function returns
    # True and false otherwise.
    for i in range(0, len(boats)):
        cur_boat = boats[i]
        if cur_boat == (boat_coord[0], boat_coord[1]):
            if side == 'L':
                if board[cur_boat[0]][cur_boat[1] - 1] == ' ':
                    board[cur_boat[0]][cur_boat[1] - 1] = '*'
                    boats[i] = (cur_boat[0], cur_boat[1] - 1)
                    new_boat = Boat()
                    new_boat.move(boats[i])
                    all_sprites.add(new_boat)
                    return True
            elif side == 'R':
                if board[cur_boat[0]][cur_boat[1] + 1] == ' ':
                    board[cur_boat[0]][cur_boat[1] + 1] = '*'
                    boats[i] = (cur_boat[0], cur_boat[1] + 1)
                    new_boat = Boat()
                    new_boat.move(boats[i])
                    all_sprites.add(new_boat)
                    return True
    return False


def move_boat_down(boat_loc):
    # This function checks if a boat can move
    # down and if so, performs the operation.
    # Returns the coordinates of the boat whether
    # it moved or not.
    space = board[boat_loc[0] + 1][boat_loc[1]]
    new_y = boat_loc[0] + 1
    new_x = boat_loc[1]

    if space == ' ':
        board[new_y][new_x] = '*'
        board[boat_loc[0]][boat_loc[1]] = ' '
        new_water = Water()
        new_water.move((boat_loc[0], boat_loc[1]))
        all_sprites.add(new_water)
        new_coords = (new_y, new_x)
        new_boat = Boat()
        new_boat.move((new_coords[0], new_coords[1]))
        all_sprites.add(new_boat)
        if board[new_coords[0] + 1][new_coords[1]] == 'M':
            board[new_y+1][new_x] = 'W'
            print_board()
            hugh.die()
            return boat_loc, True
    elif space == '*':
        if move_boat_across((new_y, new_x), 'R') \
                or move_boat_across((new_y, new_x), 'L'):
            board[new_y][new_x] = '*'
            board[boat_loc[0]][boat_loc[1]] = ' '
            new_water = Water()
            new_water.move((boat_loc[0], boat_loc[1]))
            all_sprites.add(new_water)
            new_coords = (new_y, new_x)
            new_boat = Boat()
            new_boat.move((new_coords[0], new_coords[1]))
            all_sprites.add(new_boat)
        else:
            new_coords = boat_loc
    else:
        new_coords = boat_loc

    return new_coords, False


def move_manatee(coords, move, ply_score, hyacinths):
    # This function takes the user input for the manatee
    # and moves the manatee, waits, or aborts. If the player
    # chooses to move the manatee, this function checks to
    # make sure it can, and if so makes the move. This
    # function returns the coordinates of the manatee,
    # the number of hyacinths remaining, and the score.
    space = ''
    new_x = 0
    new_y = 0
    if move == 'U':
        space = board[coords[0] - 1][coords[1]]
        new_y = coords[0] - 1
        new_x = coords[1]
    elif move == 'D':
        space = board[coords[0] + 1][coords[1]]
        new_y = coords[0] + 1
        new_x = coords[1]
    elif move == 'L':
        space = board[coords[0]][coords[1] - 1]
        new_y = coords[0]
        new_x = coords[1] - 1
    elif move == 'R':
        space = board[coords[0]][coords[1] + 1]
        new_y = coords[0]
        new_x = coords[1] + 1
    elif move == 'A':
        ply_score = ply_score + ((maxHyacinths - numHyacinths) * 25)
        return coords, hyacinths, ply_score, True

    if space == ' ' or space == '.':
        board[new_y][new_x] = 'M'
        board[coords[0]][coords[1]] = ' '
        new_water = Water()
        new_water.move((coords[0], coords[1]))
        all_sprites.add(new_water)
        new_coords = (new_y, new_x)
        return new_coords, hyacinths, ply_score, False
    elif space == '*' and (move == 'L' or move == 'R'):
        if move_boat_across((new_y, new_x), move):
            board[new_y][new_x] = 'M'
            board[coords[0]][coords[1]] = ' '
            new_water = Water()
            new_water.move((coords[0], coords[1]))
            all_sprites.add(new_water)
            new_coords = (new_y, new_x)
            return new_coords, hyacinths, score, False
        return coords, hyacinths, score, False
    elif space == '\\':
        board[new_y][new_x] = 'M'
        board[coords[0]][coords[1]] = ' '
        new_water = Water()
        new_water.move((coords[0], coords[1]))
        all_sprites.add(new_water)
        new_coords = (new_y, new_x)
        hyacinths -= 1
        ply_score += 25
        return new_coords, hyacinths, ply_score, False
    elif space == 'O':
        board[new_y][new_x] = 'M'
        board[coords[0]][coords[1]] = ' '
        new_water = Water()
        new_water.move((coords[0], coords[1]))
        all_sprites.add(new_water)
        new_coords = (new_y, new_x)
        overtext = myfont.render(f'Win', 1, (0, 0, 0))
        ply_score = ply_score + (maxHyacinths * 50)
        return new_coords, hyacinths, ply_score, True
    else:
        return coords, hyacinths, score, False


def print_board():
    # This function prints the board
    # to the standard output.
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            stdout.write(f'{board[i][j]}')
        stdout.write(f'\n')


class Hugh(pygame.sprite.Sprite):
    """A sprite for Hugh Manatee"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hugh.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(manatee[1]*50, manatee[0]*50))

    def move(self):
        self.rect = self.surf.get_rect(center=(manatee[1]*50, manatee[0]*50))

    def die(self):
        self.image = pygame.image.load("injured.png")


class Boat(pygame.sprite.Sprite):
    """A sprite to represent the boats"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boat.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(0, 0))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))


class Coquina(pygame.sprite.Sprite):
    """A sprite to represent the Coquina"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coquina.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(0, 0))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))


class Seagrass(pygame.sprite.Sprite):
    """A sprite to represent the sea grass"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("seagrass.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(0, 0))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))


class Hyacinth(pygame.sprite.Sprite):
    """A sprite to represent the hyacinths"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hyacinth.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(0, 0))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))


class Gate(pygame.sprite.Sprite):
    """A sprite to represent the gate"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("grate.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(gate[1] * 50, gate[0] * 50))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))

    def open(self):
        self.image = pygame.image.load("open.png")


class Water(pygame.sprite.Sprite):
    """A sprite to represent the empty water"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("water.png")
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(0, 0))

    def move(self, coords):
        self.rect = self.surf.get_rect(center=(coords[1] * 50, coords[0] * 50))


# This code takes in the arguments from the
# command line and opens the file within
# the URL.
parser = ArgumentParser()
parser.add_argument('--map')
args = parser.parse_args()
url = request.urlopen(args.map)
lines = url.readlines()

# This code creates the necessary variables
# and creates the game board.
board = []
boats = []
grasses = []
coquinas = []
hyacinths = []
water = []
gameOver = False
endText = 'Win'
score = 0

create_board(lines, board, boats, hyacinths, grasses, coquinas, water)
numHyacinths = len(hyacinths)
maxHyacinths = numHyacinths
gameWidth = (len(board) * 50) + 200
gameLength = len(board[0]) * 50

# This block of code initializes pygame
# and creates the elements that form the
# basis of the screen.
pygame.init()
screen = pygame.display.set_mode((gameWidth, gameLength))
white = (255, 255, 255)
screen.fill(white)
myfont = pygame.font.SysFont("monospace", 16)
scoretext = myfont.render(f'Score: {score}', 1, (0, 0, 0))
screen.blit(scoretext, (gameWidth - 200, 0))
hyatext = myfont.render(f'Hyacinths Left: {numHyacinths}', 1, (0, 0, 0))
screen.blit(hyatext, (gameWidth - 200, 50))
FPS = 30
FramePerSec = pygame.time.Clock()
FramePerSec.tick(FPS)


# Finds the coordinates of M and G and stores
# them in the variable manatee and gate
# respectively as a tuple.
for i in range(0, len(board)):
    for j in range(0, len(board[i])):
        if board[i][j] == 'M':
            manatee = (i, j)

for i in range(0, len(board)):
    for j in range(0, len(board[i])):
        if board[i][j] == 'G':
            gate = (i, j)


hugh = Hugh()
gate = Gate()
boatSprites = []
grassSprites = []
coquinaSprites = []
hyacinthSprites = []
waterSprites = []
for i in range(0, len(boats)):
    boatSprites.append(Boat())
    boatSprites[i].move(boats[i])
for i in range(0, len(grasses)):
    grassSprites.append(Seagrass())
    grassSprites[i].move(grasses[i])
for i in range(0, len(coquinas)):
    coquinaSprites.append(Coquina())
    coquinaSprites[i].move(coquinas[i])
for i in range(0, len(hyacinths)):
    hyacinthSprites.append(Hyacinth())
    hyacinthSprites[i].move(hyacinths[i])
for i in range(0, len(water)):
    waterSprites.append(Water())
    waterSprites[i].move(water[i])

all_sprites = pygame.sprite.Group()
all_sprites.add(hugh)
all_sprites.add(gate)

for boatSprite in boatSprites:
    all_sprites.add(boatSprite)
for grassSprite in grassSprites:
    all_sprites.add(grassSprite)
for coquinaSprite in coquinaSprites:
    all_sprites.add(coquinaSprite)
for hyacinthSprite in hyacinthSprites:
    all_sprites.add(hyacinthSprite)
for waterSprite in waterSprites:
    all_sprites.add(waterSprite)

all_sprites.add(hugh)

# This block of code is the main game loop
# and updates the screen, takes the user input,
# moves the manatee, moves the boats, and
# opens the gate if all the hyacinths are eaten.
while not gameOver:

    # This block of code updates the sprites and text
    # on the pygame screen.
    userInput = ' '
    pygame.event.pump()
    FramePerSec.tick(FPS)
    screen.fill(white)
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    screen.blit(hugh.image, hugh.rect)
    scoretext = myfont.render(f'Score: {score}', 1, (0, 0, 0))
    screen.blit(scoretext, (gameWidth - 200, 0))
    hyatext = myfont.render(f'Hyacinths Left: {numHyacinths}', 1, (0, 0, 0))
    screen.blit(hyatext, (gameWidth - 200, 50))
    pygame.display.update()

    # This block of code gets the user
    # input from pygame in order to determine
    # what to do later on.
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_l:
                userInput = 'L'
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_r:
                userInput = 'R'
            elif event.key == pygame.K_DOWN or event.key == pygame.K_d:
                userInput = 'D'
            elif event.key == pygame.K_UP or event.key == pygame.K_u:
                userInput = 'U'
            elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
                userInput = 'W'
            elif event.key == pygame.K_a:
                userInput = 'A'

    # This block of code is run if the user
    # input is not empty and runs through the
    # code to perform a single turn in the game.
    if userInput != ' ':
        manatee, numHyacinths, score, gameOver = \
            move_manatee(manatee, userInput, score, numHyacinths)
        score -= 1
        hugh.move()

        if gameOver:
            if userInput == 'A':
                endText = "Quit"
            continue

        for i in range(0, len(boats)):
            boatSprites[i].move(boats[i])

        if numHyacinths == 0:
            for i in range(0, len(board)):
                for j in range(0, len(board[i])):
                    if board[i][j] == 'G':
                        board[i][j] = 'O'
                        gate.open()

        for i in range(0, len(boats)):
            boats[i], gameOver = move_boat_down(boats[i])
            if gameOver:
                endText = "Lose"
                break

# This block of code prints out
# the final state of the game including
# the score and game over condition.
screen.fill(white)
for entity in all_sprites:
    screen.blit(entity.image, entity.rect)
screen.blit(hugh.image, hugh.rect)
scoretext = myfont.render(f'Score: {score}', 1, (0, 0, 0))
screen.blit(scoretext, (gameWidth - 200, 0))
hyatext = myfont.render(f'Hyacinths Left: {numHyacinths}', 1, (0, 0, 0))
screen.blit(hyatext, (gameWidth - 200, 50))
overtext = myfont.render(f'{endText}', 1, (0, 0, 0))
screen.blit(overtext, (gameWidth - 200, 100))
pygame.display.update()

# Suspends the game in a paused state
# to allow the player to view the
# outcome of the game. When a key is
# pressed the game ends.
gameOver = False
while not gameOver:
    pygame.event.pump()
    FramePerSec.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            exit(1)
