import sys
import pygame as pg
from pygame.locals import *
from board import Board
import levelreader as reader
import colors

SCREEN_WIDTH, SCREEN_HEIGHT = 550, 500

BLOCK_SIZE = 50

def render(screen, board):
    board.render(screen, BLOCK_SIZE)

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

def main():
    pg.init()
    clock = pg.time.Clock()

    board = reader.create_board_from_file("pseudo/lvl")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pg.display.set_caption('Gyro')

    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            board.person.move_left()
        elif keys[pg.K_RIGHT]:
            board.person.move_right()

        if keys[pg.K_a]:
            board.move_pipes_down(colors.BLUE)
        else:
            board.move_pipes_up(colors.BLUE)

        if keys[pg.K_s]:
            board.move_pipes_down(colors.RED)
        else:
            board.move_pipes_up(colors.RED)

        board.resolve_collisions()

        render(screen, board)
        pg.display.update()

if __name__ == '__main__': main()
