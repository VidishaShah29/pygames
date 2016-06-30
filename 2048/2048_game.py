import numpy as np
import pygame, sys
from pygame.locals import *
from board import Board

pygame.init()
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

board = Board(4, 4, max_random_value=4)
print(board.matrix)

FONT = pygame.font.SysFont("Arial", 12)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT = 20

MARGIN = 5

clock = pygame.time.Clock()

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                if event.key == pygame.K_LEFT:
                    moved = board.move("left")
                elif event.key == pygame.K_RIGHT:
                    moved = board.move("right")
                elif event.key == pygame.K_UP:
                    moved = board.move("up")
                elif event.key == pygame.K_DOWN:
                    moved = board.move("down")

                if moved:
                    board.insert_random_tile()
                    print(board.matrix, "\n")

                    if board.check_gameover():
                        print("GAME OVER!")
                        pygame.quit()
                        sys.exit()
                else:
                    print("\nCannot move to this direction!")

    screen.fill(BLACK)

    for row in range(board.shape[0]):
        for column in range(board.shape[1]):
            color = WHITE
            if board.matrix[row, column] == 0:
                color = RED

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

            drawText(screen,
                     str(board.matrix[row, column]),
                     BLACK,
                     [(MARGIN + WIDTH) * column + MARGIN,
                      (MARGIN + HEIGHT) * row + MARGIN,
                      WIDTH,
                      HEIGHT],
                     FONT)

    clock.tick(60)
    pygame.display.flip()