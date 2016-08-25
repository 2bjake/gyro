import sys
import pygame as pg
from pygame.locals import *
from board import Board
from editorpanel import EditorPanel
import levelreader as reader
import colors

SCREEN_WIDTH, SCREEN_HEIGHT = 750, 500

EDITOR_WIDTH = 100

def render(screen, board, editor=None):
    screen.fill(colors.BLACK)
    board.render(screen)
    if editor:
        editor.render(screen)

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

def toggle_editor(editor_mode, board):
    editor_mode = not editor_mode

    if editor_mode:
        board.set_screen_rect(pg.Rect(EDITOR_WIDTH, 0, SCREEN_WIDTH - EDITOR_WIDTH, SCREEN_HEIGHT))
    else:
        board.set_screen_rect(pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    return editor_mode

def main():
    pg.init()
    clock = pg.time.Clock()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    pg.display.set_caption('GyroMine')

    screen_rect = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    #level = "rope"
    #level = "scrolling_colorful"
    level = "big"
    #level = "empty"
    block_matrix, person_pos = reader.create_from_file("levels/" + level)
    board = Board(screen_rect, block_matrix, person_pos)

    editor_mode = False
    editor = EditorPanel(pg.Rect(0, 0, EDITOR_WIDTH, SCREEN_HEIGHT))

    time = 0

    while True:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == QUIT or is_key_event(event, KEYUP, K_q):
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o):
                board.person.reset()
            if is_key_event(event, KEYUP, K_e):
                editor_mode = toggle_editor(editor_mode, board)

        if editor_mode:
            (left, middle, right) = pg.mouse.get_pressed()
            if left:
                (click_x, click_y) = pg.mouse.get_pos()
                board.add_pipe_at(click_x, click_y, colors.RED)

        if time == 0 or time % 3 == 0:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                board.person.move_left(editor_mode)
            elif keys[pg.K_RIGHT]:
                board.person.move_right(editor_mode)
            elif keys[pg.K_UP]:
                board.person.move_up(editor_mode)
            elif keys[pg.K_DOWN]:
                board.person.move_down(editor_mode)

            if not editor_mode:
                board.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
                board.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
                board.move_pipes(colors.YELLOW, keys[pg.K_y])
                board.move_pipes(colors.GREEN, keys[pg.K_g])
                board.resolve_collisions()

            board.adjust_view_port()

        if editor_mode:
            render(screen, board, editor)
        else:
            render(screen, board)
        pg.display.update()
        time += 1

if __name__ == '__main__': main()
