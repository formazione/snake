from functions.soundinit import play, random_play
from functions.costants import *
import random

'''
funtions:
    - soundinit.py
        initialize sounds and let you play with play and random_play
        play need the name of the file as argument
        random_play does not need argument, but you can specify a number for randomness
    - snake.py
        the class that gives the starting position of the snake, builds the
        snake.body list with the coordinates of the parts, add a new part or
        moves it forward, check if it eats or goes out of the borders
'''
class Snake():
    def __init__(self):
        "I made the method so I can call it to restart"
        self.start()



    def start(self):
        "Where the snake starts and snake.body first list build"
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
        "A new"
        global music

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
            # not popping the last element, it grows in size
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            # A random not at a random time and random volume
            return 0

        if music:
            print("music is on")
            random_play(rnd=random.randrange(3, 10))

    def check_collisions(self):
        "Check if it goes out or on himself"
        global cnt
        
        game_over_points = (
        self.x >= 20 or self.x < 0,
        self.y > 20 or self.y < 0,
        [x for x in self.body[4:] if (self.x, self.y) == x]
        )
        if any(game_over_points):
            cnt = 0
            return 1
        else:
            return 0

#                         2 main objects
snake = Snake()

def blit_all(food_pos):
    "blit xy body and tail, altogether, uses build_snake to make the snake, \
    like we did in the menu"
    global blacktail, body, fruit, bscore2

    list_of_sprites = []
    text_surface = write(f"{score}", food_pos[0] * BOARD_SIZE + 5, food_pos[1] * BOARD_SIZE + 3, color="Black")
    btext = (text_surface, (food_pos[0] * BOARD_SIZE + 5, food_pos[1] * BOARD_SIZE + 3))
    b_score = write(f"Score: {score}", 0, 0)
    bscore = (b_score, (0, 0))
    b_score2 = (bscore2, (0, 0))
    bfruit = (fruit, (food_pos[0] * BLOCK_SIZE, food_pos[1] * BLOCK_SIZE))
    # Appending the snake body surfaces to the list of sprites
    list_of_sprites.extend(build_snake(list_of_sprites, snake.body))
    # Append the rest of the surfaces
    for surface in (bfruit, btext, b_score2, bscore):
        list_of_sprites.append(surface)
    # Blit the sequence of surfaces and coordinates 
    window.blits(blit_sequence=(list_of_sprites))
    big(window)

font = pygame.font.SysFont("Arial", 14)
def write(text_to_show, x=0, y=0, middle=0, color="Coral"):
    'To write some text on the screen for the menu and the score \
    if middle = 0, will put the text at 0,0 unless you specify coordinates \
    if middle = 1 it will put in the middle (on top)'
    text = font.render(text_to_show, 1, pygame.Color(color))
    w = h = BOARD_SIZE * BLOCK_SIZE
    if middle:
        text_rect = text.get_rect(center=((w // 2, h // 2)))
        text.blit(text, text_rect)
    else:
        text.blit(text, (x, y))
    pygame.display.update()
    return text


def build_snake(list_of_sprites, snake):
    'Builds the snake getting the coordinate from snake.body and blitting \
    a square on every coordinate, it also 2 squares for the eyes'
    btail = (blacktail, (snake[-1][0] * BLOCK_SIZE, snake[-1][1] * BLOCK_SIZE))
    for n, pos in enumerate(snake):
        # bxy = (xy, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
        if n == 0:
            bbody = (head, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
        else:
            bbody = (body, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE))
        list_of_sprites.append(bbody)

    snake_body = [bbody, btail]
    return snake_body


def big(_window):
	"Pass the surface that you want to scale on the screen Surface"
	screen.blit(pygame.transform.scale(_window, (800, 800)), (0, 0))

xs = 5
ys = 6
cnt = 0
def show_snake():
    'show the snake for the menu'
    global cnt
    global xs, ys
    if xs < 21:
        xs += .1
    else:
        xs = 5
    psnake = [[xs, ys],[xs-1, ys], [xs-2, ys]]
    l = []
    s = build_snake(l, psnake)
    l.extend(s)
    if cnt == 0:
        l.append([fruit, (380, random.randrange(120, 280, 20))])
        l.append([fruit, (380, random.randrange(120, 280, 20))])
        l.append([fruit, (380, random.randrange(120, 280, 20))])
        l.append([fruit, (380, random.randrange(120, 280, 20))])
    cnt = 1
    window.blits(blit_sequence=(l))
    big(window)
    pygame.display.update()


def menu():
    "This is the menu that waits you to click the s key to start"
    global GAME_SPEED, score, xs, ys
    xs = 5
    pygame.display.set_caption("Python Snake v. 1.8.8")
    window.blit(write("PYTHON SNAKE 2020 - MADE WITH PYGAME", middle=1), (0, 30))
    window.blit(write("Press s to start", middle=1), (0, 60))
    window.blit(write("Press m to start / stop the music", 0, 0), (0, 90))
    window.blit(write("Use the arrow keys to move the snake in the game", 0, 0), (0, 310))
    window.blit(write("Move the mouse to hear some music", 0, 0), (0, 330))
    window.blit(write("and make the snake move in the menu", 0, 0), (0, 350))
    window.blit(write("Music is experimental", 0, 0), (0, 380))
    pygame.draw.line(window, (255, 255, 255), (0, 25), (400, 25), 2)
    pygame.draw.line(window, (255, 255, 255), (0, 110), (400, 110), 2)
    big(window)
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
                score = 0
                GAME_SPEED = 8
                window.fill((0, 0, 0))
                snake.start()
                start()
        pygame.display.update()
        clock.tick(GAME_SPEED)
    pygame.quit()

music = 0
def start():
    "Once you press the 's' key it runs, moves the snake a wait the user input"
    global GAME_SPEED, score, loop, music

    go = "RIGHT"
    food_pos = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
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
                    music = 1
                if event.key == pygame.K_s:
                	save_image(window)
                snake.not_backwards(go)
        # Moves and check if eats
        if snake.move(food_pos):
            play("click")
            score += 1
            GAME_SPEED += 1
            food_pos = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        # Draw everything on
        blit_all(food_pos)
        if snake.check_collisions() == 1:
            loop = 0
            window.fill((0, 0, 0))
            menu()
        pygame.display.update()
        clock.tick(GAME_SPEED)
    pygame.quit()

menu()
