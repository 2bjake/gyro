import sys
import pygame as pg
from pygame.locals import *
from board import Board

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500

BLOCK_SIZE = 100

NUM_HORIZ_BLOCKS = SCREEN_WIDTH / BLOCK_SIZE
NUM_VERT_BLOCKS = SCREEN_HEIGHT / BLOCK_SIZE

def render(screen, board):
    board.render(screen, BLOCK_SIZE)

def main():
    pg.init()
    clock = pg.time.Clock()

    board = Board(NUM_HORIZ_BLOCKS, NUM_VERT_BLOCKS)

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pg.display.set_caption('Gyro')

    while True:
        clock.tick(50)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        render(screen, board)
        pg.display.update()

if __name__ == '__main__': main()
