import pygame

clock = pygame.time.Clock()
# Define Constants
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
screen = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE * 2, BOARD_SIZE * BLOCK_SIZE * 2))
window = pygame.Surface((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
score = 0
global music
music = 0
# SURFACES

# head = pygame.Surface((20, 20))
# head.fill((255, 255, 0))
head = pygame.image.load("imgs/head20.png").convert()
body = pygame.image.load("imgs/skin20.png").convert()
blacktail = pygame.image.load("imgs/tail.png").convert()


# fruit = pygame.Surface((20, 20))
# fruit.fill((255, 0, 0))
fruit = pygame.image.load("imgs/apple2.png").convert()
fruit.set_colorkey((255, 255, 255))
bscore2 = pygame.Surface((80, 15))
bscore2.fill((0, 0, 0))

def save_image(screen: pygame.Surface, name: str="screenshot.png"):
    "Saves an image of the screen;\
    arg 1 screen surface, arg 2 name to save"
    pygame.image.save(screen, name)