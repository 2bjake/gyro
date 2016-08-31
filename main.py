import sys
import pygame as pg
from pygame.locals import *
from board import Board
from person import Person
import pipe
from editorpanel import EditorPanel
import levelfile
import colors
from blocks import *

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

    EDITOR_WIDTH = 100

    #LEVEL = "rope"
    #LEVEL = "scrolling_colorful"
    #LEVEL = "kara"
    LEVEL = "empty"

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), 0, 32)

        pg.display.set_caption('GyroMine')

        self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

        block_matrix, person_pos = levelfile.create_from_file("levels/" + Game.LEVEL)
        self.board = Board(self.board_screen_rect, block_matrix)
        self.pipes = pipe.create_pipes(self.board)
        self.person = Person(self.board, person_pos)

        self.editor_mode = False
        self.editor_screen_rect = pg.Rect(0, 0, Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        self.editor = EditorPanel(self.editor_screen_rect)

    def render(self):
        self.screen.fill(colors.BLACK)
        self.board.render(self.screen)
        self.render_pipes()
        self.person.render(self.screen)
        if self.editor_mode:
            self.editor.render(self.screen)

    def render_pipes(self):
        #render pipe details
        #TODO: figure out the right way to do this without getting board internals
        # not sure i need to do this min, make adjust_view_port always make view_rect the right values
        # and then this code can just use it
        max_x = min(self.board.matrix_rect.right, self.board.view_rect.right)
        for color in self.pipes:
            for pipe in self.pipes[color]:
                if self.board.view_rect.left <= pipe.x < max_x: # could use collidepoint
                    pipe.render(self.screen)


    def toggle_editor(self):
        self.editor_mode = not self.editor_mode

        #TODO: make these rects contants?
        if self.editor_mode:
            self.board_screen_rect = pg.Rect(Game.EDITOR_WIDTH, 0, Game.SCREEN_WIDTH - Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        else:
            self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
            #TODO: move the person to somewhere safe

        self.board.set_screen_rect(self.board_screen_rect)

    def handle_mouse_events(self):
        (left, middle, right) = pg.mouse.get_pressed()

        if not left and not right:
            return

        click_pos = pg.mouse.get_pos()

        if self.board_screen_rect.collidepoint(click_pos):
            if left:
                block = self.editor.get_selected_block()
            elif right:
                block = EmptyBlock()
            block_added = self.board.add_block_at(click_pos, block)
            if block_added:
                self.pipes = pipe.create_pipes(self.board)
        elif self.editor_screen_rect.collidepoint(click_pos):
            self.editor.handle_click(click_pos)

    def handle_keystroke_events(self):
        for event in pg.event.get():
            if event.type == QUIT or is_key_event(event, KEYUP, K_q):
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o):
                self.person.reset()
            if is_key_event(event, KEYUP, K_p):
                self.toggle_editor()
            if is_key_event(event, KEYUP, K_x):
                p = self.person
                levelfile.write_to_file(self.board.block_matrix, p.x, p.y)

    def move_pipes(self, color, down):
        for pipe in self.pipes[color]:
            pipe.move(down)

    def resolve_collisions(self): #also handles falling which isn't really collisions...
        block_at_person = self.board.get_block(self.person.x, self.person.y)
        block_below_person = self.board.get_block(self.person.x, self.person.y - 1)

        if block_at_person.is_solid:
            if self.person.can_move(self.person.x, self.person.y + 1):
                self.person.move_up()
            else:
                self.person.kill()
        elif not block_below_person.is_solid and not isinstance(block_at_person, RopeBlock):
            self.person.move_down()

    def run(self):
        time = 0

        while True:
            self.clock.tick(60)

            # handle keystroke events
            self.handle_keystroke_events()

            # handle mouse events
            if self.editor_mode:
                self.handle_mouse_events()

            # handle held down key events
            if time == 0 or time % 3 == 0:
                keys = pg.key.get_pressed()
                # person movement
                if keys[pg.K_LEFT]:
                    self.person.move_left(self.editor_mode)
                elif keys[pg.K_RIGHT]:
                    self.person.move_right(self.editor_mode)
                elif keys[pg.K_UP]:
                    self.person.move_up(self.editor_mode)
                elif keys[pg.K_DOWN]:
                    self.person.move_down(self.editor_mode)

                # pipe movement
                if not self.editor_mode:
                    self.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
                    self.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
                    self.move_pipes(colors.YELLOW, keys[pg.K_y])
                    self.move_pipes(colors.GREEN, keys[pg.K_g])
                    self.resolve_collisions()

            self.board.adjust_view_port(self.person.x)
            self.render()
            pg.display.update()
            time += 1

def main():
    Game().run()

if __name__ == '__main__': main()
