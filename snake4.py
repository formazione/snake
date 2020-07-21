import pygame
from pygame import gfxdraw
import sys
import random
from functions.soundinit import init

'''
Snake 1.4
- add sound
- add score


'''

clock = pygame.time.Clock()
# Define Constants
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
window = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
score = 0

class Snake():
    def __init__(self):
        "I made the method so I can call it to restart"
        self.start()

    def start(self):
        self.head = [5, 5]
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0] - 1, self.head[1]],
                     [self.head[0] - 2, self.head[1]]
                     ]
        self.direction = "RIGHT"

    def change_direction_to(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, food_pos):
        if self.direction == "RIGHT":
            self.head[0] += 1
        if self.direction == "LEFT":
            self.head[0] -= 1
        if self.direction == "UP":
            self.head[1] -= 1
        if self.direction == "DOWN":
            self.head[1] += 1
        self.body.insert(0, list(self.head))
        if self.head == food_pos:
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            return 0

    def check_collision(self):
        "Check if it goes out or on himself"
        game_over_points = (
        self.head[0] >= 20 or self.head[0] < 0,
        self.head[1] > 20 or self.head[1] < 0,
        [x for x in self.body[1:] if self.head == x]
        )
        if any(game_over_points):
            return 1
        else:
            return 0


class FoodSpawner():
    def __init__(self):
        self.rnd_spot = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        self.is_food_on_screen = True

    def spawn_food(self):
        if self.is_food_on_screen == False:
            self.is_food_on_screen = True
            self.rnd_spot = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
            write(f"{score}", self.rnd_spot[0] * BOARD_SIZE, self.rnd_spot[1]* BOARD_SIZE)
        return self.rnd_spot

    def set_food_on_screen(self, bool_value):
        self.is_food_on_screen = bool_value


#                         2 main objects
snake = Snake()
food_spawner = FoodSpawner()

body = pygame.Surface((20, 20))
body.fill((255, 255, 0))
blacktail = pygame.Surface((20, 20))
blacktail.fill((0, 0, 0))
fruit = pygame.Surface((20, 20))
fruit.fill((255, 0, 0))

bscore2 = pygame.Surface((80, 15))
bscore2.fill((0, 0, 0))
def blit_all(food_pos):
    "blit head body and tail, altogether"
    global blacktail, body, fruit, bscore2

    list_of_sprites = []
    # head = 1
    btail = (blacktail, (snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE))
    text_surface = write(f"{score}", food_pos[0] * BOARD_SIZE + 5, food_pos[1] * BOARD_SIZE + 3, color="Black")
    btext = (text_surface, (food_pos[0] * BOARD_SIZE + 5, food_pos[1] * BOARD_SIZE + 3))
    b_score = write(f"Score: {score}", 0, 0)
    bscore = (b_score, (0, 0))
    b_score2 = (bscore2, (0, 0))
    for pos in snake.body:
        # bhead = (head, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
        bbody = (body, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
        bfruit = (fruit, (food_pos[0] * BLOCK_SIZE, food_pos[1] * BLOCK_SIZE))
        # if head == 1:
        #     list_of_sprites.append(head)
        #     head = 0
        # else:
        list_of_sprites.append(bbody)
        list_of_sprites.append(btail)
        list_of_sprites.append(bfruit)
        list_of_sprites.append(btext)
        list_of_sprites.append(b_score2)
        list_of_sprites.append(bscore)


    window.blits(blit_sequence=(list_of_sprites))



def write(text_to_show, x=0, y=0, middle=0, color="Coral"):
    font = pygame.font.SysFont(text_to_show, 24)
    text = font.render(text_to_show, 1, pygame.Color(color))
    w = h = BOARD_SIZE * BLOCK_SIZE
    if middle:
        text_rect = text.get_rect(center=((w // 2, h // 2)))
        text.blit(text, text_rect)
    else:
        text.blit(text, (x, y))
    pygame.display.update()
    return text



def restart():
    global GAME_SPEED, score

    score = 0
    GAME_SPEED = 8
    window.fill((0, 0, 0))
    snake.start()
    start()


def press_to_start():
    global loop

    init("sounds")
    window.blit(write("Press s to start", middle=1), (200, 200))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            loop = 0
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = 0
                break
            if event.key == pygame.K_s:
                restart()
                break
    pygame.quit()



def start():
    global GAME_SPEED, score, loop

    food_pos = food_spawner.spawn_food()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction_to("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_direction_to("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction_to("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction_to("LEFT")
        if snake.move(food_pos) == 1:
            score += 1
            food_spawner.set_food_on_screen(False)
            GAME_SPEED += 1
            food_pos = food_spawner.spawn_food()
            # text_rect = text 

        blit_all(food_pos)

        # draw_fruit(food_pos)

        if snake.check_collision() == 1:
            loop = 0
            press_to_start()
        pygame.display.update()
        clock.tick(GAME_SPEED)

    pygame.quit()

press_to_start()
