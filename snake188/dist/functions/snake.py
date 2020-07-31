from functions.costants import *
from functions.soundinit import play, random_play

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
        game_over_points = (
        self.x >= 20 or self.x < 0,
        self.y > 20 or self.y < 0,
        [x for x in self.body[4:] if (self.x, self.y) == x]
        )
        if any(game_over_points):
            return 1
        else:
            return 0

#                         2 main objects
snake = Snake()