import pygame
from pygame import gfxdraw
import sys
import random


clock = pygame.time.Clock()
# Define Constants
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
HEAD_COLOR = (0, 100, 0)  # Dark Green
BODY_COLOR = (0, 200, 0)  # Light Green
FOOD_COLOR = (200, 0, 0)  # Dark Red
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
window = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
score = 0

class Snake():
    def __init__(self):
        self.start()


    def start(self):
        self.head = [int(BOARD_SIZE / 4), int(BOARD_SIZE / 4)]
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
        ''' Move the snake to the desired direction by adding the head to that direction
            and remove the tail if the snake does not eat food
        '''
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
        conditions = (
        self.head[0] >= 20 or self.head[0] < 0,
        self.head[1] > 20 or self.head[1] < 0,
        [x for x in self.body[1:] if self.head == x]
        )
        if any(conditions):
            return 1
        else:
            return 0


class FoodSpawner():
    def __init__(self):
        self.head = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        self.is_food_on_screen = True

    def spawn_food(self):
        if self.is_food_on_screen == False:
            self.head = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
            self.is_food_on_screen = True
        return self.head

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

def blit_all(food_pos):
    "blit head body and tail, altogether"
    global blacktail, body, fruit

    list_of_sprites = []
    # head = 1
    btail = (blacktail, (snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE))
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


    window.blits(blit_sequence=(list_of_sprites))


pygame.init()


def write(text_to_show, x=0, y=0, middle=0):
    font = pygame.font.SysFont(text_to_show, 24)
    text = font.render(text_to_show, 1, pygame.Color("Coral"))
    w = h = BOARD_SIZE * BLOCK_SIZE
    if middle:
        text_rect = text.get_rect(center=((w // 2, h // 2)))
        window.blit(text, text_rect)
    else:
        window.blit(text, (x, y))
    pygame.display.update()


def restart():
    global GAME_SPEED

    GAME_SPEED = 8
    window.fill((0, 0, 0))
    snake.start()
    start()


def press_to_start():
    global loop
    write("Press any s to start", middle=1)
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
            # delete_fruit(pos, food_pos)
            score += 1
            food_spawner.set_food_on_screen(False)
            GAME_SPEED += 1
            food_pos = food_spawner.spawn_food()

        blit_all(food_pos)

        # draw_fruit(food_pos)

        if snake.check_collision() == 1:
            loop = 0
            press_to_start()
        pygame.display.update()
        clock.tick(GAME_SPEED)

    pygame.quit()

press_to_start()
