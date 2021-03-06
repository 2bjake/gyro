import sys
import os
import pygame as pg
from pygame.locals import *
import levelfile
import colors
from point import Point
from view import View
from blocks import EmptyBlock

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

class Main:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.view = View(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
        self.levels = os.listdir("levels")
        self.level_index = 0
        self.load_level(self.levels[self.level_index])

    def load_next_level(self):
        self.level_index = (self.level_index + 1) % len(self.levels)
        self.load_level(self.levels[self.level_index])

    def load_level(self, level_name):
        self.game_state = levelfile.create_from_file("levels/" + level_name)

    def handle_mouse_events(self):
        (left, middle, right) = pg.mouse.get_pressed()

        if not left and not right:
            return

        click_pos = Point(*pg.mouse.get_pos())

        board_screen_rect = self.view.get_board_screen_rect(self.game_state.editor_enabled)
        if board_screen_rect.collidepoint(click_pos): #TODO consider moving this into method on view is_in_board_screen(pos, editor_enabled)
            if left:
                block = self.game_state.editor.get_selected_block()
            elif right:
                block = EmptyBlock()
            board_pos = self.view.get_board_position_for_screen_position(click_pos, self.game_state.editor_enabled)
            self.game_state.add_block(block, board_pos)
        elif self.view.get_editor_screen_rect().collidepoint(click_pos):
            block_index = self.view.get_editor_selection_index_for_click(click_pos, self.game_state.editor)
            if block_index is not None:
                self.game_state.editor.index = block_index

    def handle_keystroke_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o): # reset
                self.game_state.reset()
            if is_key_event(event, KEYUP, K_l): # load next level
                self.load_next_level()
            if is_key_event(event, KEYUP, K_p): # toggle editor
                self.game_state.toggle_editor()
            if is_key_event(event, KEYUP, K_x): # save level
                level_name = self.view.ask_for_level_name()
                levelfile.write_to_file(self.game_state, level_name)
                self.levels.append(level_name)
                self.level_index = len(self.levels) - 1
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
                    if self.game_state.game_win:
                        self.load_next_level()

            self.view.render(self.game_state)
            pg.display.update()
            time += 1

def main():
    Main().run()

if __name__ == '__main__': main()
