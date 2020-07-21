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


class Snake():
    def __init__(self):
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
     return 1



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


# Game Initialization
window = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
fps = pygame.time.Clock()

score = 0

# Initialize snake and food
snake = Snake()
food_spawner = FoodSpawner()



def game_over():
    pygame.display.set_caption("SNAKE GAME  |  Score: " + str(score) + "  |  GAME OVER. Press any key to quit ...")
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            break
    pygame.quit()
    #sys.exit()

def delete_fruit():
        gfxdraw.filled_circle(window, food_pos[0] * BLOCK_SIZE + 10, food_pos[1] * BLOCK_SIZE + 10, 9, (0, 0, 0))

def draw_fruit():
        gfxdraw.filled_circle(window, food_pos[0] * BLOCK_SIZE + 10, food_pos[1] * BLOCK_SIZE + 10, 9, (255, 0, 0))

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
        delete_fruit()
        score += 1
        food_spawner.set_food_on_screen(False)
        GAME_SPEED += 1
        food_pos = food_spawner.spawn_food()


    # window.fill(pygame.Color(225, 225, 225))
    # Draw snake
    head = 1
    for pos in snake.body:
        if head == 1:
            pygame.draw.rect(window, (0, 255, 0),
                             pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            head = 0
        else:
            pygame.draw.rect(window, (BODY_COLOR),
                             pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    # Draw food
    # gfxdraw.filled_circle(screen, ball.x, ball.y, 6, self.color)
    draw_fruit()
    # pygame.draw.rect(window, FOOD_COLOR,
    #                  pygame.Rect(food_pos[0] * BLOCK_SIZE, food_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


    #pygame.display.set_caption("SNAKE GAME  |  Speed: " + str(GAME_SPEED) + "  |  Score: " + str(score))
    pygame.display.flip()
    clock.tick(GAME_SPEED)
    if snake.check_collision() == 1:
        game_over()
        loop = 0

pygame.quit()
