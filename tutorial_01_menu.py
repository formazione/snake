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
        "The starting menu waitin to press s"
        Game.write("Press s to start", middle="both")

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                if event.key == pygame.K_s:
                    print("Start")
                    break
        pygame.quit()

    def write(t, x: int = 0, y: int = 0, middle: str = "both", color="Coral") -> pygame.Surface:
        text = Game.render_text(t, color)
        if middle == "both":
            rect_middle = text.get_rect(center=((Game.WIDTH // 2, Game.HEIGHT //2)))
            Game.screen.blit(text, rect_middle)
        else:
            Game.screen.blit(text, (x, y))
        pygame.display.update()
        return text

    def render_text(t: str, color: str) -> pygame.Surface:
        "Renders a text and return it as a Surface"
        text = Game.font.render(t, 1, pygame.Color(color))
        return text


Game.menu()
