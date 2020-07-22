import pygame
from pygame import gfxdraw
import sys
import random


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
        self.start()


    def start(self):
        # coordinates of the head 5, 5
        self.head = [
            int(BOARD_SIZE / 4), # x = self.head[0] = 5 = 20 / 4
            int(BOARD_SIZE / 4)] # y ? self.head[1] = 5 = 20 / 4
        # self.head[0] = x = 5
        # self.head[1] = x = 5
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0] - 1, self.head[1]],
                     [self.head[0] - 2, self.head[1]]
                     ]
        #   [ ][ ][ ] => right
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
        ''' Move the snake to the desired
        direction by adding the head to that direction
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
        # [][][]
        self.body.insert(0, list(self.head))
        # [][][][]
        if self.head == food_pos:
            # [][][][]  it grows after he ate
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            # pop([])   [][][]  it stays of the same size, but moves
            return 0

    def check_collision(self):
        # Checks collision with border or himself

        conditions = (
            # x axis limits  <0 ..... >20
            self.head[0] >= 20 or self.head[0] < 0,
            # y axis
            self.head[1] > 19 or self.head[1] < 0,
            # checks if you hit yourself
            # comprehension list - a for loop with a python syntax
            [x for x in self.body[1:] if self.head == x]
        )
        if any(conditions):
            return 1
        else:
            return 0


class FoodSpawner():
    def __init__(self):
        self.food_pos = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        self.is_food_on_screen = True

    def spawn_food(self):
        if self.is_food_on_screen == False:
            self.food_pos = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
            self.is_food_on_screen = True
        return self.food_pos

    def set_food_on_screen(self, bool_value):
        self.is_food_on_screen = bool_value


#                         2 main objects


def draw_head(pos):
    pygame.draw.rect(
        window,
        (0, 255, 0),
        pygame.Rect(
            pos[0] * BLOCK_SIZE,
            pos[1] * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE))


def draw_body(pos):
    pygame.draw.rect(window, (0, 128, 0), pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def delete_tail(pos):
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def delete_fruit(pos, food_pos):
    x = food_pos[0] * BLOCK_SIZE + 10
    y = food_pos[1] * BLOCK_SIZE + 10
    r = 9
    gfxdraw.filled_circle(window, x, y, r, (0, 0, 0))


def draw_fruit(food_pos):
    gfxdraw.filled_circle(window, food_pos[0] * BLOCK_SIZE + 10, food_pos[1] * BLOCK_SIZE + 10, 9, (255, 0, 0))


# To write on the window surface on the screen

def write(text_to_show, x=0, y=0, middle="both"):
    "It write in the middle by default, if not middle='both' middle='x'"
    text = font.render(text_to_show, 1, pygame.Color("Coral"))
    if middle == "x":
        text_rect = text.get_rect(center=((size // 2, y)))
        window.blit(text, text_rect)      
    elif middle == "both":
        text_rect = text.get_rect(center=((size // 2, size // 2)))
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
    "Initial menu"
    global loop, snake, food_spawner
    global font, size

    pygame.init()
    font = pygame.font.SysFont("Arial", 24)
    size = BOARD_SIZE * BLOCK_SIZE # 400 20x20
    snake = Snake()
    food_spawner = FoodSpawner()
    write("Python vs Snake", y=30, middle="x")
    write("Press s to start")
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
    "Starts the game"
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

        head = 1
        for pos in snake.body:
            if head == 1:
                draw_head(pos)
                head = 0
            else:
                draw_body(pos)
        delete_tail(pos)
        draw_fruit(food_pos)

        if snake.check_collision() == 1:
            loop = 0
            press_to_start()
        pygame.display.update()
        clock.tick(GAME_SPEED)

    pygame.quit()

press_to_start()
