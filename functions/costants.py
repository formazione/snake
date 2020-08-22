import pygame
from functions.snake import *
import os


def list_fruit():
    "Used by Costants.FRUITS to store names and surface of fruits"
    fruits = []
    for img in os.listdir("imgs/fruits/"):
        fname = img[:-4]
        fruit = pygame.image.load("imgs/fruits/" + img).convert_alpha()
        fruit.set_colorkey((255, 255, 255))
        fruits.append((fname, fruit))
    return fruits

class Costants:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (128, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (255, 255, 255)
    COLORS = (BLACK, RED, GREEN, YELLOW, ORANGE, BLUE, GRAY)
    
    clock = pygame.time.Clock()
    # Define Constants
    BOARD_SIZE = 20  # Size of the board, in block
    BLOCK_SIZE = 20  # Size of 1 block, in pixel
    GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
    screen = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE * 2, BOARD_SIZE * BLOCK_SIZE * 2))
    window = pygame.Surface((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
    pygame.display.set_caption("Snake 2.0.3")
    score = 0
    music = 0
    w, h = window.get_size()
    w2 = w // 2
    h2 = h // 2

    # this are blitted with blit_all function
    # make a tuple tup_fly(fly, (0, 0)) and go
    head = pygame.image.load("imgs/head20.png").convert_alpha()
    redhead = pygame.image.load("imgs/headred.png").convert_alpha()
    redbody = pygame.image.load("imgs/skinred.png").convert_alpha()
    body = pygame.image.load("imgs/skin20.png").convert_alpha()
    blacktail = pygame.image.load("imgs/tail.png").convert_alpha()
    # clean = pygame.Surface((300, 20))
    # clean.fill((128, 64, 0))
    # Create list of different fruits to choose with choice
    FRUITS = list_fruit()
    fly = pygame.image.load("imgs/fly2.png").convert_alpha()

    # Obscure score and maxscore text
    bscore1 = pygame.Surface((400, 20))
    bscore1.fill((128, 64, 0))



def save_image(screen: pygame.Surface, name: str="screenshot.png"):
    "Saves an image of the screen;\
    arg 1 screen surface, arg 2 name to save"
    pygame.image.save(screen, name)

def replace_Costants(filename):
    w = "screen,window,score,music,head,body,blacktail,fruit,bscore2"
    w = w.split(",")
    print(w)

    with open(filename, "r") as file:
        testo = file.read()
#    print(testo)
    for eachword in w:
        testo = testo.replace(eachword, "Costants." + eachword)
    print(testo)
    # with open(filename, "w") as file:
    #     file.write(testo)

if __name__ == "__main__":
    replace_Costants("../snake189.py")
