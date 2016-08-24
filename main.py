import sys
import pygame as pg
from pygame.locals import *
from board import Board
import levelreader as reader
import colors

SCREEN_WIDTH, SCREEN_HEIGHT = 750, 500

def render(screen, board):
    screen.fill(colors.BLACK)
    board.render(screen)

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

def main():
    pg.init()
    clock = pg.time.Clock()

    #level = "rope"
    #level = "scrolling_colorful"
    level = "big"
    board = reader.create_board_from_file("levels/" + level)
    board.view_width = SCREEN_WIDTH / 50 #TODO: this is weird, remove it and instead provide rect for display area
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pg.display.set_caption('GyroMine')

    time = 0

    while True:
        clock.tick(60)
        time += 1
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o):
                board.person.reset()

        #HACK: do this for real
        (left, middle, right) = pg.mouse.get_pressed()
        if left:
            (click_x, click_y) = pg.mouse.get_pos()
            board.add_pipe_at(click_x, click_y, colors.RED)


        if time % 3 == 0:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                board.person.move_left()
            elif keys[pg.K_RIGHT]:
                board.person.move_right()
            elif keys[pg.K_UP]:
                board.person.move_up()
            elif keys[pg.K_DOWN]:
                board.person.move_down()

            board.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
            board.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
            board.move_pipes(colors.YELLOW, keys[pg.K_y])
            board.move_pipes(colors.GREEN, keys[pg.K_g])

            board.resolve_collisions()
            board.adjust_view_port()

        render(screen, board)
        pg.display.update()

if __name__ == '__main__': main()
