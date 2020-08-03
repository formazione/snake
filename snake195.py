from functions.soundinit import play, random_play
from functions.costants import *
from functions.score import *
import random



class Snake():
    def __init__(self):
        "I made the method so I can call it to restart"
        self.start()

    def start(self):
        "Where the snake starts and Costants.snake.body first list build"
        self.x = 5
        self.y = 5
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

    def move(self, food_pos):
        global fruit, fruitname

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
        if [self.x, self.y] == food_pos:
            random_play()
            
            # Write what you eat
            if fruitname == "banana":
                fruitname ="banana: go slow!"
            text = write(f"You ate : {fruitname}", 300, 0)
            text_rect = text.get_rect(center=((Costants.w2, 10)))
            Costants.window.blit(Costants.clean, text_rect)
            Costants.window.blit(text, text_rect)

            if fruitname == "cherry":
                self.body = self.body[:3]

            # whe you eat banana you do not grow
            if fruitname == "banana: go slow!":
                if len(self.body) > 3:
                    self.body.pop()
                    if Costants.GAME_SPEED > 8:
                        Costants.GAME_SPEED -= 1
                    # self.body.pop()

                play("banana")
            fruit = random.choice(Costants.FRUITS)
            fruitname, fruit = fruit

            # not popping the last element, it grows in size
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            # A random not at a random time and random volume
            return 0

        if Costants.music:
            print("music is on")
            random_play(rnd=random.randrange(3, 10))

    def check_collisions(self):
        "Check if it goes out or on himself"
        global cnt, game

        game_over_points = (
        self.x >= 20 or self.x < 0,
        self.y > 20 or self.y < 0,
        [x for x in self.body[1:] if [self.x, self.y] == x]
        )
        if any(game_over_points):
            game.save_score(Costants.score)
            cnt = 0
            gameover()
            return 1
        else:
            return 0


def number_on_apple(food_pos):
    text_surface = write(f"{Costants.score + 1}", food_pos[0] * Costants.BOARD_SIZE + 5, food_pos[1] * Costants.BOARD_SIZE + 3, color="Black")
    btext = (text_surface,
        (food_pos[0] * Costants.BOARD_SIZE + 5, food_pos[1] * Costants.BOARD_SIZE + 3))
    return btext

def add(content):
    global list_of_tuples
    list_of_tuples.append(content)

def blit_all(food_pos):
    "Create all the tuples for Costants.window.blits blit_sequence"
    global game, list_of_tuples, fruit

    list_of_tuples = []
    
    #  -Creates the number on the apple
    # - add score
    # - add maxscore
    # - add surfaces to hide score
    # - add mosquito
    # - add fruit

    # Hide score and maxscore
    add((Costants.bscore1, (0, 0)))
    add((Costants.bscore2, (300, 0)))
    add((write(f"Score: {Costants.score}", 0, 0), (20, 0)))
    b_maxiscore = write(f"Max-score: {game.maxscore}", 0, 0)
    add((b_maxiscore, (300, 0)))
    # The fly
    add((Costants.fly, (0,0)))
    # fruit and number
    add((fruit, (food_pos[0] * Costants.BLOCK_SIZE, food_pos[1] * Costants.BLOCK_SIZE)))
    # add((number_on_apple(food_pos)))
    # Snake
    list_of_tuples.extend(build_snake(list_of_tuples, snake.body))

    Costants.window.blits(blit_sequence=(list_of_tuples))
    big(Costants.window)


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


def build_snake(list_of_sprites, _snake):
    'Builds the snake getting the coordinate from Costants.snake.body and blitting \
    a square on every coordinate, it also 2 squares for the eyes'
    btail = (Costants.blacktail, (_snake[-1][0] * Costants.BLOCK_SIZE, _snake[-1][1] * Costants.BLOCK_SIZE))
    for n, pos in enumerate(_snake):
        # bxy = (xy, (pos[0] * Costants.BLOCK_SIZE, pos[1] * Costants.BLOCK_SIZE))
        if n == 0:
            bhead = (Costants.head, (pos[0] * Costants.BLOCK_SIZE, pos[1] * Costants.BLOCK_SIZE))
        else:
            bbody = (Costants.body, (pos[0] * Costants.BLOCK_SIZE, pos[1] * Costants.BLOCK_SIZE))
            list_of_sprites.append(bbody)

    snake_body = [bhead, bbody, btail]
    return snake_body


def big(_window):
	"Pass the surface that you want to scale on the Costants.screen Surface"
	Costants.screen.blit(pygame.transform.scale(_window, (800, 800)), (0, 0))

xs = 5
ys = 6



def show_snake():
    'show the snake for the menu'
    global cnt, fruit
    global xs, ys
    bfruit = pygame.Surface((20, 20))
    bfruit.fill((0, 0, 0))
    def show_fruits():
        cnt = 0
        for i in range(4):
            if cnt == 0:
                fruit = random.choice(Costants.FRUITS)
                fruit = fruit[1]
                yrnd = random.randrange(120, 280, 20)
                l.append([bfruit, (380, yrnd)])
                l.append([fruit, (380, yrnd)])
        cnt = 1


    if xs < 21:
        xs += .1
    else:
        xs = 5
    psnake = [[xs, ys], [xs-1, ys], [xs-2, ys]]
    l = []
    s = build_snake(l, psnake)
    l.extend(s)
    show_fruits()
    Costants.window.blits(blit_sequence=(l))
    big(Costants.window)
    pygame.display.update()


def menu():
    "This is the menu that waits you to click the s key to start"
    global xs, ys, game, fruit, fruitname
    # this will game.maxscore = 10... for example
    game = Score("score.txt")
    xs = 5
    pygame.display.set_caption("Python Snake v. 1.8.8")
    Costants.window.blit(write("PYTHON SNAKE 2020 - MADE WITH PYGAME", middle=1), (0, 30))
    Costants.window.blit(write("Press s to start", middle=1), (0, 60))
    Costants.window.blit(write("Max - Score " + str(game.maxscore), middle=1), (0, 90))
    # Costants.window.blit(write("Press m to start / stop the music", 0, 0), (0, 90))
    Costants.window.blit(write("Use the arrow keys to move the snake in the game", 0, 0), (0, 310))
    Costants.window.blit(write("Move the mouse to hear some music", 0, 0), (0, 330))
    Costants.window.blit(write("and make the snake move in the menu", 0, 0), (0, 350))
    Costants.window.blit(write("Music is experimental", 0, 0), (0, 380))
    pygame.draw.line(Costants.window, (255, 255, 255), (0, 25), (400, 25), 2)
    pygame.draw.line(Costants.window, (255, 255, 255), (0, 110), (400, 110), 2)
    big(Costants.window)
    loop1 = 1
    while loop1:
        show_snake()
        random_play()
        event = pygame.event.wait()
        if (event.type == pygame.QUIT):
            break
        if event.type == pygame.KEYDOWN:
            press_escape = event.key == pygame.K_ESCAPE
            if press_escape:
                break
            restart = (event.key == pygame.K_s)
            if restart:
                Costants.score = 0
                Costants.GAME_SPEED = 8
                Costants.window.fill((0, 0, 0))
                snake.start()
                fruit = random.choice(Costants.FRUITS)
                fruitname, fruit = fruit
                start()
        pygame.display.update()
        Costants.clock.tick(Costants.GAME_SPEED)
    pygame.quit()


snake = Snake()
Costants.music = 0
def start():
    "Once you press the 's' key it runs, moves the snake a wait the user input"
    global loop

    go = "RIGHT"
    food_pos = [random.randrange(1, Costants.BOARD_SIZE), random.randrange(1, Costants.BOARD_SIZE)]
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
        if snake.move(food_pos):
            play("click")
            Costants.score += 1
            if Costants.score > int(game.maxscore):
                game.maxscore = str(Costants.score)
                #game.save_score(Costants.score)
            Costants.GAME_SPEED += .5
            food_pos = [random.randrange(1, Costants.BOARD_SIZE), random.randrange(1, Costants.BOARD_SIZE)]
        # Draw everything on
        blit_all(food_pos)
        if snake.check_collisions() == 1:
            loop = 0
            Costants.window.fill((0, 0, 0))
            menu()
        pygame.display.update()
        Costants.clock.tick(Costants.GAME_SPEED)
    pygame.quit()


def gameover():
    def surface(redux):
        main = pygame.Surface((Costants.w - redux, Costants.h - redux))
        if (redux // 20) % 2 == 0:
            main.fill((0,0,0))
        else:
            main.fill((64, 64, 64))
        Costants.window.blit(main, (redux, redux))
        Costants.screen.blit(pygame.transform.scale(main, ((Costants.w - redux) * 2, (Costants.h - redux) * 2)), (redux, redux))
        # pygame.time.delay(5)
        pygame.display.update()
        Costants.clock.tick(20)


    play("over")
    for x in range(20):
        surface(x * 20)


menu()