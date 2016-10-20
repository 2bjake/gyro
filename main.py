import sys
import pygame as pg
from pygame.locals import *
from board import Board
from characters import *
from goals import *
import pipe
from editorpanel import EditorPanel
import levelfile
import colors
from blocks import *
from point import *

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

    EDITOR_WIDTH = 80

    #LEVEL = "rope"
    #LEVEL = "scrolling_colorful"
    LEVEL = "jess_first"
    #LEVEL = "empty"

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), 0, 32)

        pg.display.set_caption('GyroMine')

        self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

        block_matrix, person_pos, smick_pos_list, coin_pos_list = levelfile.create_from_file("levels/" + Game.LEVEL)
        #TODO move game state data into separate class
        self.board = Board(self.board_screen_rect, block_matrix)
        self.pipes = pipe.create_pipes(self.board)
        self.person = Person(self.board, person_pos)

        self.smicks = {}
        for smick_pos in smick_pos_list:
            self.smicks[smick_pos] = Smick(self.board, smick_pos)

        self.coins = {}
        self.total_coin_count = len(coin_pos_list)
        self.set_available_coin_count(self.total_coin_count)
        for coin_pos in coin_pos_list:
            self.coins[coin_pos] = Coin(self.board, coin_pos)

        self.editor_mode = False
        self.editor_screen_rect = pg.Rect(0, 0, Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        self.editor = EditorPanel(self.editor_screen_rect)

    def render(self):
        self.screen.fill(colors.BLACK)
        self.board.render(self.screen)
        self.render_pipes()
        self.person.render(self.screen)

        for smick in self.smicks.values():
            smick.render(self.screen)

        for coin in self.coins.values():
            coin.render(self.screen)

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
                if self.board.view_rect.left <= pipe.top_pos.x < max_x: # could use collidepoint
                    pipe.render(self.screen)


    def toggle_editor(self):
        self.editor_mode = not self.editor_mode

        #TODO: make these rects contants?
        if self.editor_mode:
            self.board_screen_rect = pg.Rect(Game.EDITOR_WIDTH, 0, Game.SCREEN_WIDTH - Game.EDITOR_WIDTH, Game.SCREEN_HEIGHT)
        else:
            self.board_screen_rect = pg.Rect(0, 0, Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
            #TODO: move the person to somewhere safe
        self.person.set_start_pos()
        self.reset_game()
        self.board.set_screen_rect(self.board_screen_rect)

    def handle_mouse_events(self):
        (left, middle, right) = pg.mouse.get_pressed()

        if not left and not right:
            return

        click_pos = Point(*pg.mouse.get_pos())

        if self.board_screen_rect.collidepoint(click_pos):
            if left:
                block = self.editor.get_selected_block()
            elif right:
                block = EmptyBlock()
            block_added = self.board.add_block_at(click_pos, block)
            if block_added:
                self.pipes = pipe.create_pipes(self.board)
                if block.is_solid:
                    matrix_pos = self.board.screen_coords_to_matrix_coords(click_pos)
                    self.toggle_smick(matrix_pos)
                    self.toggle_coin(matrix_pos)
        elif self.editor_screen_rect.collidepoint(click_pos):
            self.editor.handle_click(click_pos)

    def handle_keystroke_events(self):
        for event in pg.event.get():
            if event.type == QUIT or is_key_event(event, KEYUP, K_q):
                pg.quit()
                sys.exit()
            if is_key_event(event, KEYUP, K_o): # reset
                self.reset_game()
            if is_key_event(event, KEYUP, K_p): # toggle editor
                self.toggle_editor()
            if is_key_event(event, KEYUP, K_x): # save level
                self.person.set_start_pos()
                levelfile.write_to_file(self.board.block_matrix, self.person, self.smicks, self.coins)
            if is_key_event(event, KEYUP, K_s) and self.editor_mode: # toggle smick (only in editor mode)
                self.toggle_smick(self.person.pos)
            if is_key_event(event, KEYUP, K_c) and self.editor_mode: # toggle coin (only in editor mode)
                self.toggle_coin(self.person.pos)

    def move_pipes(self, color, down):
        for pipe in self.pipes[color]:
            pipe.move(down)

    def move_character(self, character):
        block_at_character = self.board.get_block(character.pos)

        block_below_character = self.board.get_block(point_down(character.pos))

        if block_at_character.is_solid:
            if character.can_move(point_up(character.pos)):
                character.move_up()
            else:
                character.kill()
        elif not block_below_character.is_solid and not isinstance(block_at_character, RopeBlock):
            character.move_down()

    def toggle_smick(self, pos):
        existing_smick = self.smicks.pop(pos, None)
        if existing_smick == None and not self.board.get_block(pos).is_solid:
            self.smicks[pos] = Smick(self.board, pos)

    def toggle_coin(self, pos):
        existing_coin = self.coins.pop(pos, None)
        if existing_coin == None:
            if not self.board.get_block(pos).is_solid:
                self.coins[pos] = Coin(self.board, pos)
                self.total_coin_count += 1
        else:
            self.total_coin_count -= 1
        self.set_available_coin_count(self.total_coin_count)

    def set_available_coin_count(self, count):
        self.available_coin_count = count
        print(self.available_coin_count)

        if self.available_coin_count == 0:
            pass #open the door
        else:
            pass #close the door

    def reset_game(self):
        self.person.reset()
        self.reset_smicks()
        self.reset_coins()

    def reset_smicks(self):
        for smick in self.smicks.values():
            smick.reset()

    def reset_coins(self):
        self.set_available_coin_count(self.total_coin_count)
        for coin in self.coins.values():
            coin.reset()

    def resolve_deaths(self):
        for smick in self.smicks.values():
            if smick.is_alive and smick.pos == self.person.pos:
                self.person.kill()

    def resolve_goals(self):
        coin = self.coins.get(self.person.pos)
        if coin is not None and coin.is_available:
            coin.is_available = False
            self.set_available_coin_count(self.available_coin_count - 1)

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

                if not self.editor_mode:
                    self.move_pipes(colors.BLUE, keys[pg.K_a] or keys[pg.K_b])
                    self.move_pipes(colors.RED, keys[pg.K_s] or keys[pg.K_r])
                    self.move_pipes(colors.YELLOW, keys[pg.K_y])
                    self.move_pipes(colors.GREEN, keys[pg.K_g])
                    self.move_character(self.person)
                    for smick in self.smicks.values():
                        if smick.is_alive:
                            self.move_character(smick)
                    self.resolve_deaths()
                    self.resolve_goals()

            self.board.adjust_view_port(self.person.pos.x)
            self.render()
            pg.display.update()
            time += 1

def main():
    Game().run()

if __name__ == '__main__': main()
