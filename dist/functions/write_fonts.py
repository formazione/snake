import pygame


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