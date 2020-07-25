import pygame

clock = pygame.time.Clock()
# Define Constants
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
window = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
score = 0
global music
music = 0
# SURFACES

head = pygame.Surface((20, 20))
head.fill((255, 255, 0))
head2 = pygame.Surface((5, 5))
head2.fill((255, 0, 0))

body = pygame.Surface((20, 20))
body.fill((0, 255, 0))
blacktail = pygame.Surface((20, 20))
blacktail.fill((0, 0, 0))
fruit = pygame.Surface((20, 20))
fruit.fill((255, 0, 0))

bscore2 = pygame.Surface((80, 15))
bscore2.fill((0, 0, 0))