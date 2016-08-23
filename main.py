import sys
import pygame as pg
from pygame.locals import *
from board import Board
import levelreader as reader

SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 700

BLOCK_SIZE = 100

def render(screen, board):
    board.render(screen, BLOCK_SIZE)

def main():
    pg.init()
    clock = pg.time.Clock()

    board = reader.create_board_from_file("pseudo/lvl")

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
