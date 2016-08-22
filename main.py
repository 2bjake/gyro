import sys
import random
import pygame as pg
from pygame.locals import *
import colors

screenWidth, screenHeight = 800, 500

width, height = 8, 5 
blocks = [[colors.WHITE for y in range(height)] for x in range(width)]

def renderBlock(screen, blockX, blockY):
    blockWidth = screenWidth / (width * 1.0)
    blockHeight = screenHeight / (height * 1.0)
    rect = ((blockWidth * blockX, blockHeight * blockY), (blockWidth, blockHeight));
    pg.draw.rect(screen, blocks[blockX][blockY], rect)

def render(screen):
    for x in range(width):
        for y in range(height):
            renderBlock(screen, x, y)

def main():
    pg.init()
    clock = pg.time.Clock()

    screen = pg.display.set_mode((screenWidth, screenHeight), 0, 32)
    pg.display.set_caption('Gyro')

    while True:
        clock.tick(50)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        screen.fill(colors.BLACK)
        render(screen)
        pg.display.update()

if __name__ == '__main__': main()
