import sys
import pygame as pg
from pygame.locals import *
from board import Board
import levelreader as reader
import colors

SCREEN_WIDTH, SCREEN_HEIGHT = 750, 500

BLOCK_SIZE = 50

def render(screen, board):
    screen.fill(colors.BLACK)
    board.render(screen, BLOCK_SIZE)

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

def main():
    pg.init()
    clock = pg.time.Clock()

    level = "rope"
    board = reader.create_board_from_file("levels/" + level)
    board.set_view_width(SCREEN_WIDTH / BLOCK_SIZE)
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
        elif keys[pg.K_UP]:
            board.person.move_up()
        elif keys[pg.K_DOWN]:
            board.person.move_down()

        if keys[pg.K_a] or keys[pg.K_b]:
            board.move_pipes_down(colors.BLUE)
        else:
            board.move_pipes_up(colors.BLUE)

        if keys[pg.K_s] or keys[pg.K_r]:
            board.move_pipes_down(colors.RED)
        else:
            board.move_pipes_up(colors.RED)

        if keys[pg.K_y]:
            board.move_pipes_down(colors.YELLOW)
        else:
            board.move_pipes_up(colors.YELLOW)

        if keys[pg.K_g]:
            board.move_pipes_down(colors.GREEN)
        else:
            board.move_pipes_up(colors.GREEN)


        board.resolve_collisions()
        board.adjust_view_port()

        render(screen, board)
        pg.display.update()

if __name__ == '__main__': main()
