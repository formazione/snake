import pygame
from random import randrange

class Snake(pygame.sprite.Sprite):
    """docstring for Snake"""
    head = pygame.image.load("imgs/head.png")
    skin = pygame.image.load("imgs/skin.png")
    tail = pygame.Surface((5, 5))
    tail.fill((0, 0, 0))

    def __init__(self):
        self.direction = "right"
        self.x = 5 * 20
        self.y = 5 * 20
        self.head = Snake.head
        self.skin = Snake.skin
        self.tail = Snake.tail
        self.body = [
            [self.head, self.x, self.y],
            [self.skin, self.x - 5, self.y],
            [self.skin, self.x - 10, self.y],
            [self.skin, self.x - 15, self.y]
        ]


snake = Snake()
print(snake.body)
class Game:
    "Starts the game"
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    WIDTH: int = 600
    HEIGHT: int = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 16)
    display = pygame.Surface((WIDTH // 4, HEIGHT // 4))
    clock = pygame.time.Clock()
    row = randrange(1, 20)
    col = randrange(1, 20)
    pos_food = [row * 20, col * 20]
    count = 0
    # used by Game.move()
    move_to = {
        "right": .5,
        "left": -.5,
        "up": -.5,
        "down": .5}

    def menu() -> None:
        "PRESS S TO START"
        Game.write('Snake', 0, 0, middle="")
        Game.write("Press s to start", 0, 20, middle="")
        # Wait the user to press 's' or to quit / escape
        while True:
            event = pygame.event.wait()
            if pygame.event.get(pygame.QUIT):
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                break
            if keys[pygame.K_s]:
                print("Start")
                Game.display.fill((0, 0, 0))
                Game.start()
                # break
        pygame.quit()


    def write(t, x: int = 0, y: int = 0, middle: str = "both", color="Coral") -> pygame.Surface:
        "RENDERS AND BLIT THE TEXT ====================\
        Examples to display text on the screen:  \
        - Write in the middle:           \
        Game.write('Game over')         \
        - write everywhere:          \
        Game.write('Snake', 0, 0, middle='')"
        text = Game.font.render(t, 1, pygame.Color(color))
        if middle == "both":
            rect_middle = text.get_rect(center=((Game.WIDTH // 2, Game.HEIGHT // 2)))
            Game.display.blit(text, rect_middle)
        else:
            Game.display.blit(text, (x, y))
        Game.screen.blit(pygame.transform.scale(Game.display, (600, 600)), (0,0))
        pygame.display.update()
        return text


    def start():

        go = "right"

        # a random posizion multiple of 20
        
        loop = 1
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                    # You cannot move backwards
                    elif event.key == pygame.K_RIGHT:
                        go = "right"
                    elif event.key == pygame.K_UP:
                        go = "up"
                    elif event.key == pygame.K_DOWN:
                        go = "down"
                    elif event.key == pygame.K_LEFT:
                        go = "left"
            Game.not_back(go)
            Game.move()
            Game.blit_all()
            Game.screen.blit(pygame.transform.scale(Game.display, (600, 600)), (0,0))
            pygame.display.update()
            Game.clock.tick(8)
        pygame.quit()

    def not_back(wanna_go):
        "Avoid going backwards and moves"
        Game.count += 1
        if Game.count == 4:
            Game.count = 0
            if wanna_go in "left right":
                if snake.direction in "up down":
                    snake.direction = wanna_go
            # IF YOU GO LEFT OR RIGHT YOU CAN GO UP OR DOWN
            elif snake.direction in "left right":
                snake.direction = wanna_go
            # ========= goes to the next step =====



    def move():
        if snake.direction in "right left":

                snake.x += Game.move_to[snake.direction] * 5

        else:

                snake.y += Game.move_to[snake.direction] * 5


        Game.add_head()
        Game.check_eat()

    def check_eat():
        if [snake.x, snake.y] == Game.pos_food:
            return 1
        else:
            snake.body.pop()
            return 0

    def add_head():
        snake.body.insert(0, [snake.head, snake.x, snake.y])
        # snake.body.pop(1)
        snake.body[1] = [snake.skin, snake.body[1][1], snake.body[1][2]]

    def blit_all():
        "Blits all the sprites and surfaces"
        Game.display.blits(blit_sequence=Game.build_snake())

    def build_snake():
        "Creates the sequence to be blitted"
        seq_snake = []
        for n in snake.body:
            srf, x, y = n
            seq = (srf, (x, y))
            seq_snake.append(seq)
        seq_snake.append((snake.tail, (snake.body[-1][1], snake.body[-1][2])))
        return seq_snake

Game.menu()
