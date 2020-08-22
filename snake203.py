from functions.soundinit import *
from functions.costants import *
from functions.score import *
import random
import numpy as np

# pysnake 2.0.0

class Square:
    def __init__(self):
        self.start()

    def start(self):
        self.matrix = np.zeros(shape=(20, 20), dtype=np.int)

square = Square()
class Snake():
    def __init__(self):
        "I made the method so I can call it to restart"
        self.start()
        # number of square to fill to change stage 380

    def start(self):
        "Where the snake starts and Costants.snake.body first list build"
        self.square_count = 0
        # you need to eat 10 food to change level
        self.food_eaten = 0
        self.stamina_max = 40
        self.stamina = self.stamina_max
        self.stage = 0
        self.square_target = 100
        self.food_target = 5
        self.ground_color = (73, 33, 0)
        self.start_pos()

    def start_pos(self):
        self.x = 5
        self.y = 8
        # This has the coords of the snake; head -1 -2 are the other
        self.body = [[self.x - c, self.y] for c in range(3)]
        self.moves_towards = "RIGHT"

    def not_backwards(self, wanna_go):
        "Avoid going backwards"
        if wanna_go in "LEFT RIGHT":
            if self.moves_towards in "UP DOWN":
                self.moves_towards = wanna_go
        # IF YOU GO LEFT OR RIGHT YOU CAN GO UP OR DOWN
        elif self.moves_towards in "LEFT RIGHT":
            self.moves_towards = wanna_go

    def move(self):
        global fruit, fruitname, base, list_of_tuples, eat_banana, food_pos
        # THE STEP OF HIS MOVES
        directions = {
            "RIGHT": 1,
            "LEFT": -1,
            "UP": -1,
            "DOWN": 1}
        if self.moves_towards in "RIGHT LEFT":
            self.x += directions[self.moves_towards]
        else:
            self.y += directions[self.moves_towards]

        self.body.insert(0, [self.x, self.y])



        ###################################################################
        #                                                                 #
        #          Snake gets the food    2.0.3                           #
        #                  19.08.2020                                     #
        ###################################################################
                     #
                    #

        if [self.x, self.y] == food_pos:
            # add the fruit count, stamina back to max
            self.food_eaten += 1
            # the faster you are the more your score increases
            Costants.score += self.stamina_max - self.stamina
            if fruitname == "fly":
                Costants.score += 100

            self.stamina = self.stamina_max
            #
            fruit = random.choice(Costants.FRUITS)
            # if FLY..... change position sometimes
            fruitname, fruit = fruit
            go = "RIGHT"
            return 1
        else:
            # Do not add a piece

            self.body.pop()
            return 0


    def check_collisions(self):
        "Check if it goes out or on himself"
        global cnt, game

        game_over_points = (
        self.stamina < 0,
        self.x >= 20 or self.x < 0,
        self.y > 19 or self.y < 1,
        [x for x in self.body[1:] if [self.x, self.y] == x]
        )
        if any(game_over_points):
            game.save_score(Costants.score)
            cnt = 0
            self.start()
            gameover()
            return 1
        else:
            # EAT TERRAIN
            if square.matrix[self.x][self.y] == 0:
                Costants.score += 1
                square.matrix[self.x][self.y] = 1
                self.stamina -= 1
                self.square_count += 1
                if self.stamina < 10:
                    play("click")
                    # Costants.head = pygame.image.load("imgs/head20.png")
                    # Costants.head = pygame.image.load("imgs/Costants.headred.png")
            # RESTART
            if self.square_count > self.square_target and self.food_eaten > self.food_target:
                self.square_count = 0
                self.food_eaten = 0
                self.stage += 1
                self.square_target += 20
                self.food_target += 2
                self.stamina_max = 40 - snake.stage
                self.stamina = self.stamina_max
                self.body = self.body[:3]
                # This is to detect when you dig, deleting the 1, 1, 1, 1...
                # square.start()
                Costants.GAME_SPEED = 8 + snake.stage
                play("next_level")
                snake.start_pos()
                new_stage()
                start()
                # play("dig")
            return 0


# def number_on_apple(food_pos):
#     text_surface = write(f"{Costants.score + 1}", food_pos[0] * Costants.BOARD_SIZE + 5, food_pos[1] * Costants.BOARD_SIZE + 3, color="Black")
#     btext = (text_surface,
#         (food_pos[0] * Costants.BOARD_SIZE + 5, food_pos[1] * Costants.BOARD_SIZE + 3))
#     return btext

def add(content):
    global list_of_tuples
    list_of_tuples.append(content)

def blit_all():
    "Create all the tuples for Costants.window.blits blit_sequence"
    global game, list_of_tuples, fruit, food_pos, fruitname

    list_of_tuples = []

    if fruitname == "fly":
        if random.randint(1, 5 - snake.stage // 2) == 1:
            xx, yy = food_pos
            xx, yy = xx * 20, yy * 20
            square.matrix[snake.x][snake.y] == 1
            add((Costants.blacktail, (xx, yy)))


            # food_pos = [random.randrange(1, Costants.BOARD_SIZE), random.randrange(1, Costants.BOARD_SIZE)]
            
            if random.random() < 0.5:
                if food_pos[0] > 1 or food_pos[0] < 16:
                    food_pos[0] += random.choice([-1, 1])
            else:
                if food_pos[1] > 2 or food_pos[1] < 16:
                    food_pos[1] += random.choice([-1, 1])     
                # food_pos[1] += random.randint(-1, 1)
        
    # Score
    add((Costants.bscore1, (0, 0)))
    add((write(f"Score: {Costants.score} Stamina: {snake.stamina} Terra:{snake.square_count}/{snake.square_target} Fruit: {snake.food_eaten}/{snake.food_target+1} Stage:{snake.stage}", 0, 0), (20, 0)))
    b_maxiscore = write(f"Max: {game.maxscore}", 0, 0)
    add((b_maxiscore, (350, 0)))
    # The fly
    
    #add((Costants.fly, (0,0)))

    # fruit and number
    add((fruit, (food_pos[0] * Costants.BLOCK_SIZE, food_pos[1] * Costants.BLOCK_SIZE)))
    # add((number_on_apple(food_pos)))
    # Snake
    list_of_tuples.extend(build_snake(list_of_tuples, snake.body))

    Costants.window.blits(blit_sequence=(list_of_tuples))
    big(Costants.window)

head2 = pygame.Surface((20, 20))
def build_snake(list_of_sprites, _snake):
    'Builds the snake'
    global head2

    btail = (
        Costants.blacktail,
        (
            _snake[-1][0] * Costants.BLOCK_SIZE,
            _snake[-1][1] * Costants.BLOCK_SIZE))
    
    # ALERT STAMINA
    if snake.stamina < 10:
        head2 = Costants.redhead
        body = Costants.redbody
    else:
        head2 = Costants.head
        body = Costants.body

    for n, pos in enumerate(_snake):
        if n == 0:
            bhead = (
                head2, (
                    pos[0] * Costants.BLOCK_SIZE,
                    pos[1] * Costants.BLOCK_SIZE))
        else:
            bbody = (
                body,
                (
                    pos[0] * Costants.BLOCK_SIZE,
                    pos[1] * Costants.BLOCK_SIZE))
            list_of_sprites.append(bbody)

    snake_body = [bhead, bbody, btail]

    return snake_body


font = pygame.font.SysFont("Arial", 14)


def write(text_to_show, x=0, y=0, middle=0, color="Coral"):
    'To write some text on the Costants.screen for the menu and the score \
    if middle = 0, will put the text at 0,0 unless you specify coordinates \
    if middle = 1 it will put in the middle (on top)'
    text = font.render(text_to_show, 1, pygame.Color(color))
    w = h = Costants.BOARD_SIZE * Costants.BLOCK_SIZE
    if middle:
        text_rect = text.get_rect(center=((w // 2, h // 2)))
        text.blit(text, text_rect)
    else:
        text.blit(text, (x, y))
    pygame.display.update()
    return text




def big(_window):
	"Pass the surface that you want to scale on the Costants.screen Surface"
	Costants.screen.blit(pygame.transform.scale(_window, (800, 800)), (0, 0))

xs = 5
ys = 6



def menu():
    "This is the menu that waits you to click the s key to start"
    global xs, ys, game, fruit, fruitname, base
    # this will game.maxscore = 10... for example

    game = Score("score.txt")
    xs = 5
    soundtrack(play="stop")
    Costants.window.fill(snake.ground_color)
    fruit = random.choice(Costants.FRUITS)
    fruitname, fruit = fruit
    # ======== THE SNAKE LOGO
    logo = pygame.image.load("imgs/splash.png")
    Costants.window.blit(logo, (0, 0))
    big(Costants.window)
    loop1 = 1
    while loop1:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                loop1 = 0
            if event.type == pygame.KEYDOWN:
                press_escape = event.key == pygame.K_ESCAPE
                if press_escape:
                    loop1 = 0
                # restart = (event.key == pygame.K_s)
                # if restart:
                #     Costants.score = 0
                #     Costants.GAME_SPEED = 8
                #     Costants.window.fill(snake.ground_color)
                #     snake.start()
                #     fruit = random.choice(Costants.FRUITS)
                #     fruitname, fruit = fruit

                start()
        pygame.display.update()
        Costants.clock.tick(Costants.GAME_SPEED + 52)
    pygame.quit()


snake = Snake()
Costants.music = 0
def start():
    "Once you press the 's' key it runs, moves the snake a wait the user input"
    global loop, base, food_pos

    snake.moves_towards = "RIGHT"
    square.start()
    snake.food_eaten = 0

    soundtrack()
    go = "RIGHT"
    food_pos = [random.randrange(1, Costants.BOARD_SIZE), random.randrange(1, Costants.BOARD_SIZE)]

    loop = 1
    Costants.window.fill(snake.ground_color)
    while loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                # You cannot move backwards
                elif event.key == pygame.K_RIGHT:
                    go = "RIGHT"
                elif event.key == pygame.K_UP:
                    go = "UP"
                elif event.key == pygame.K_DOWN:
                    go = "DOWN"
                elif event.key == pygame.K_LEFT:
                    go = "LEFT"
                if event.key == pygame.K_m:
                    Costants.music = 1
                if event.key == pygame.K_s:
                	save_image(Costants.window)
                snake.not_backwards(go)
        # Moves and check if eats
        if snake.move():
            play("click")
            Costants.score += 20
            if Costants.score > int(game.maxscore):
                game.maxscore = str(Costants.score)
                #game.save_score(Costants.score)
            Costants.GAME_SPEED += .5 + snake.stage / 10
            food_pos = [random.randrange(1, Costants.BOARD_SIZE), random.randrange(1, Costants.BOARD_SIZE)]
        # Draw everything on
        else:
            if snake.check_collisions() == 1:
                loop = 0
                Costants.window.fill(snake.ground_color)
                menu()
        blit_all()
        pygame.display.update()
        Costants.clock.tick(Costants.GAME_SPEED)
    pygame.quit()


def gameover():
    "Game over scene with concentric squares"
    def surface(rdx):
        sq_surf = pygame.Surface((Costants.w - rdx, Costants.h - rdx))
        sq_surf.fill((0,0,0)) if (rdx // 20) % 2 == 0 else sq_surf.fill((64, 64, 64))
        Costants.screen.blit(pygame.transform.scale(sq_surf, ((Costants.w - rdx) * 2, (Costants.h - rdx) * 2)), (rdx, rdx))
        Costants.screen.blit(write("Game Over"), (370, 400))
        pygame.display.update()
        Costants.clock.tick(20)
    play("over")
    for x in range(20):
        surface(x * 20)
    Costants.GAME_SPEED = 8
    Costants.score = 0

    pygame.event.wait()


def new_stage():
    def surface2(rdx):
        main = pygame.Surface((Costants.w - rdx, Costants.h - rdx))
        main.fill((128, 128, 128)) if (rdx // 20) % 2 == 0 else main.fill((255, 0, 0))
        Costants.screen.blit(pygame.transform.scale(main, ((Costants.w - rdx) * 2, (Costants.h - rdx) * 2)), (rdx, rdx))
        Costants.screen.blit(write("New Level"), (370, 400))
        # pygame.time.delay(5)
        pygame.display.update()
        Costants.clock.tick(10)

    play("next_level")
    for x in range(20):
        surface2(x * 20)
    pygame.event.wait()
    pygame.time.delay(1000)
    snake.moves_towards = "RIGHT"


menu()