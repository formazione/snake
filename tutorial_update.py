import pygame


class Game:
    "Starts the game"
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    WIDTH: int = 400
    HEIGHT: int = 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    def menu() -> None:
        "PRESS S TO START"
        Game.write('Snake', 0, 0, middle="")
        Game.write("Press s to start", middle="both")
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
                break
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
            rect_middle = text.get_rect(center=((Game.WIDTH // 2, Game.HEIGHT //2)))
            Game.screen.blit(text, rect_middle)
        else:
            Game.screen.blit(text, (x, y))
        pygame.display.update()
        return text


Game.menu()
