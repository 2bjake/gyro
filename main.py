import sys
import pygame as pg
from pygame.locals import *
from board import Board
from editorpanel import EditorPanel
import levelfile
import colors

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 750, 500

    EDITOR_WIDTH = 100

    #LEVEL = "rope"
    #LEVEL = "scrolling_colorful"
    LEVEL = "big"
    #LEVEL = "empty"

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), 0, 32)

        pg.display.set_caption('GyroMine')

        self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

        block_matrix, person_pos = levelfile.create_from_file("levels/" + Game.LEVEL)
        self.board = Board(self.board_screen_rect, block_matrix, person_pos)

        self.editor_mode = False
        self.editor_screen_rect = pg.Rect(0, 0, Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        self.editor = EditorPanel(self.editor_screen_rect)

    def render(self):
        self.screen.fill(colors.BLACK)
        self.board.render(self.screen)
        if self.editor_mode:
            self.editor.render(self.screen)

    def toggle_editor(self):
        self.editor_mode = not self.editor_mode

        #TODO: make these rects contants?
        if self.editor_mode:
            self.board_screen_rect = pg.Rect(Game.EDITOR_WIDTH, 0, Game.SCREEN_WIDTH - Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        else:
            self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

        self.board.set_screen_rect(self.board_screen_rect)

    def handle_edit_click(self, click_pos):
        if self.board_screen_rect.collidepoint(click_pos):
            (click_x, click_y) = pg.mouse.get_pos()
            block = self.editor.get_selected_block()
            self.board.add_block_at(click_x, click_y, block)
        elif self.editor_screen_rect.collidepoint(click_pos):
            self.editor.handle_click(click_pos)

    def run(self):
        time = 0

        while True:
            self.clock.tick(60)

            # handle keystroke events
            for event in pg.event.get():
                if event.type == QUIT or is_key_event(event, KEYUP, K_q):
                    pg.quit()
                    sys.exit()
                if is_key_event(event, KEYUP, K_o):
                    self.board.person.reset()
                if is_key_event(event, KEYUP, K_p):
                    self.toggle_editor()
                if is_key_event(event, KEYUP, K_x):
                    p = self.board.person
                    levelfile.write_to_file(self.board.block_matrix, p.x, p.y)

            # handle mouse events
            if self.editor_mode:
                (left, middle, right) = pg.mouse.get_pressed()
                if left:
                    self.handle_edit_click(pg.mouse.get_pos())

            # handle held down key events
            if time == 0 or time % 3 == 0:
                keys = pg.key.get_pressed()
                # person movement
                if keys[pg.K_LEFT]:
                    self.board.person.move_left(self.editor_mode)
                elif keys[pg.K_RIGHT]:
                    self.board.person.move_right(self.editor_mode)
                elif keys[pg.K_UP]:
                    self.board.person.move_up(self.editor_mode)
                elif keys[pg.K_DOWN]:
                    self.board.person.move_down(self.editor_mode)

                # pipe movement
                if not self.editor_mode:
                    self.board.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
                    self.board.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
                    self.board.move_pipes(colors.YELLOW, keys[pg.K_y])
                    self.board.move_pipes(colors.GREEN, keys[pg.K_g])
                    self.board.resolve_collisions()

            self.board.adjust_view_port()
            self.render()
            pg.display.update()
            time += 1

def main():
    Game().run()

if __name__ == '__main__': main()
