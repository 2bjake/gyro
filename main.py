import sys
import pygame as pg
from pygame.locals import *
import levelfile
import colors
from point import Point
from renderer import Renderer
from blocks import EmptyBlock

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

class Main:
    SCREEN_WIDTH, SCREEN_HEIGHT = 980, 500

    #LEVEL = "jess_first"
    LEVEL = "miles_first"
    #LEVEL = "empty"

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        screen = pg.display.set_mode((Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT), 0, 32)
        self.renderer = Renderer(screen, Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)

        pg.display.set_caption('GyroMine')

        self.game_state = levelfile.create_from_file("levels/" + Main.LEVEL)

    def handle_mouse_events(self):
        (left, middle, right) = pg.mouse.get_pressed()

        if not left and not right:
            return

        click_pos = Point(*pg.mouse.get_pos())

        if self.game_state.board_screen_rect.collidepoint(click_pos):
            if left:
                block = self.game_state.editor.get_selected_block()
            elif right:
                block = EmptyBlock()
            block_added = self.game_state.board.add_block_at(click_pos, block)
            if block_added:
                self.game_state.create_pipes()
                if block.is_solid:
                    matrix_pos = self.game_state.board.screen_coords_to_matrix_coords(click_pos)
                    self.game_state.toggle_smick(matrix_pos)
                    self.game_state.toggle_coin(matrix_pos)
        elif self.game_state.editor_screen_rect.collidepoint(click_pos):
            self.game_state.editor.handle_click(click_pos)

    def handle_keystroke_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o): # reset
                self.game_state.reset()
            if is_key_event(event, KEYUP, K_p): # toggle editor
                self.game_state.toggle_editor()
            if is_key_event(event, KEYUP, K_x): # save level
                levelfile.write_to_file(self.game_state)
            if is_key_event(event, KEYUP, K_s) and self.game_state.editor_enabled: # toggle smick (only in editor mode)
                self.game_state.toggle_smick(self.game_state.person.pos)
            if is_key_event(event, KEYUP, K_c) and self.game_state.editor_enabled: # toggle coin (only in editor mode)
                self.game_state.toggle_coin(self.game_state.person.pos)


    def run(self):
        time = 0

        while True:
            self.clock.tick(60)

            # handle keystroke events
            self.handle_keystroke_events()

            # handle mouse events
            if self.game_state.editor_enabled:
                self.handle_mouse_events()

            # handle held down key events
            if time == 0 or time % 3 == 0:
                keys = pg.key.get_pressed()
                # person movement
                if keys[pg.K_LEFT]:
                    self.game_state.person.move_left(self.game_state.editor_enabled)
                elif keys[pg.K_RIGHT]:
                    self.game_state.person.move_right(self.game_state.editor_enabled)
                elif keys[pg.K_UP]:
                    self.game_state.person.move_up(self.game_state.editor_enabled)
                elif keys[pg.K_DOWN]:
                    self.game_state.person.move_down(self.game_state.editor_enabled)

                if not self.game_state.editor_enabled:
                    self.game_state.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
                    self.game_state.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
                    self.game_state.move_pipes(colors.YELLOW, keys[pg.K_y])
                    self.game_state.move_pipes(colors.GREEN, keys[pg.K_g])
                    self.game_state.update_state()

            self.game_state.board.adjust_view_port(self.game_state.person.pos.x)
            self.renderer.render(self.game_state)
            pg.display.update()
            time += 1

def main():
    Main().run()

if __name__ == '__main__': main()
