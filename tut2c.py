import pygame
from random import randrange

class Snake(pygame.sprite.Sprite):
    """docstring for Snake"""
    head = pygame.image.load("imgs/head.png")
    skin = pygame.image.load("imgs/skin.png")
    delete_tail = pygame.Surface((5, 5))
    delete_tail.fill((0, 0, 0))

    def __init__(self):
        self.direction = "right"
        self.x = 1
        self.y = 0
        self.head = Snake.head
        self.skin = Snake.skin
        self.delete_tail = Snake.delete_tail
        self.cnt = 1
        self.part_direction = ["right","right","right"] # direction of each part
        self.build_body()
    def return_coord(self):
        if self.direction == "right":
            xx = 5
            yy = 0
        if self.direction == "left":
            xx = -5
            yy = 0
        if self.direction == "down":
            xx = 0
            yy = 5
        if self.direction == "up":
            xx = 0
            yy = -5
        self.part_direction[self.cnt]
        return xx, yy

    def build_body(self):
        self.body = []
        self.add()

    '''
    have to store each direction for every skin
    each skin continue going in the direction of the previous skin
    the first skin continue going in the direction of the head
    the second skin continue to the direction of the first skin...
    '''

    def add(self):
        self.cnt = 0
        xx, yy = self.return_coord()
        self.body.append([self.head, self.x - xx * self.cnt, self.y - yy * self.cnt, self.part_direction[self.cnt]])
        
        self.cnt += 1
        xx, yy = self.return_coord()
        self.body.append([self.skin, self.x - xx * self.cnt, self.y - yy * self.cnt, self.part_direction[self.cnt]])
        
        self.cnt += 1
        xx, yy = self.return_coord()
        self.body.append([self.skin, self.x - xx * self.cnt, self.y - yy * self.cnt, self.part_direction[self.cnt]])



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
        "right": 1,
        "left": -1,
        "up": -1,
        "down": 1}

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
            Game.display.fill((0,0,0))
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
            Game.clock.tick(30)
        pygame.quit()

    def not_back(wanna_go):
        "Avoid going backwards and moves"
        Game.count += 1
        if Game.count == 5:
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
                snake.x += Game.move_to[snake.direction]
        else:
                snake.y += Game.move_to[snake.direction]
        snake.build_body()
        Game.check_eat()

    def check_eat():
        if [snake.x, snake.y] == Game.pos_food:
            return 1
        else:
            snake.body.pop()
            return 0

    def blit_all():
        "Blits all the sprites and surfaces"
        Game.display.blits(blit_sequence=Game.build_snake())

    def build_snake():
        "Creates the sequence to be blitted"
        seq_snake = []
        for n in snake.body:
            srf, x, y, direct = n
            seq = (srf, (x, y))
            seq_snake.append(seq)
        # # Add the surface snake.delete_tail that delete the tail
        # # when you go right is good... but not when goes towards left up dpwn
        # if snake.direction == "right":
        #     seq_snake.append((snake.delete_tail, (snake.body[-1][1] - 5, snake.body[-1][2])))
        # if snake.direction == "left":
        #     seq_snake.append((snake.delete_tail, (snake.body[-1][1] + 5, snake.body[-1][2])))
        # if snake.direction == "up":
        #     seq_snake.append((snake.delete_tail, (snake.body[-1][1], snake.body[-1][2] + 5)))
        # if snake.direction == "down":
        #     seq_snake.append((snake.delete_tail, (snake.body[-1][1], snake.body[-1][2] - 5)))
        return seq_snake

Game.menu()
