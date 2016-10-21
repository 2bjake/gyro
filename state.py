from collections import defaultdict
import pygame as pg
from board import Board
from characters import *
from goals import *
from pipe import Pipe
from editorpanel import EditorPanel
import colors
from blocks import *
from point import *

class GameState:
    TEMP_SCREEN_WIDTH, TEMP_SCREEN_HEIGHT = 1000, 500
    TEMP_EDITOR_WIDTH = 80

    def __init__(self, block_matrix, person_pos, smick_pos_list, coin_pos_list):
        #TODO: these rects don't belong here
        self.board_screen_rect = pg.Rect(0, 0, GameState.TEMP_SCREEN_WIDTH, GameState.TEMP_SCREEN_HEIGHT)
        self.board = Board(self.board_screen_rect, block_matrix)

        self.pipes = self.create_pipes()
        self.person = Person(self.board, person_pos)

        self.smicks = {}
        for smick_pos in smick_pos_list:
            self.smicks[smick_pos] = Smick(self.board, smick_pos)

        self.coins = {}
        self.total_coin_count = len(coin_pos_list)
        self.set_available_coin_count(self.total_coin_count)
        for coin_pos in coin_pos_list:
            self.coins[coin_pos] = Coin(self.board, coin_pos)

        self.editor_enabled = False
        self.editor_screen_rect = pg.Rect(0, 0, GameState.TEMP_EDITOR_WIDTH, GameState.TEMP_SCREEN_HEIGHT)
        self.editor = EditorPanel(self.editor_screen_rect)

    def create_pipes(self):
        pipes = defaultdict(list)

        x, y = 0, 0
        while x < self.board.matrix_rect.width:
            while y < self.board.matrix_rect.height:
                pos = Point(x, y)
                block = self.board.get_block(pos)
                if isinstance(block, PipeBlock):
                    pipe = self._create_pipe(pos, block.color)
                    pipes[block.color].append(pipe)
                    y = pipe.top_pos.y
                y += 1
            x += 1
            y = 0
        return pipes

    def _create_pipe(self, bottom_pos, color):
        cur_pos = bottom_pos
        cur_block = self.board.get_block(cur_pos)
        while isinstance(cur_block, PipeBlock) and cur_block.color == color:
            cur_pos = point_up(cur_pos)
            cur_block = self.board.get_block(cur_pos)
        cur_pos = point_down(cur_pos)

        return Pipe(self.board, cur_pos, bottom_pos)

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

    def toggle_editor(self):
        self.editor_enabled = not self.editor_enabled

        #TODO: make these rects contants?
        if self.editor_enabled:
            self.board_screen_rect = pg.Rect(GameState.TEMP_EDITOR_WIDTH, 0, GameState.TEMP_SCREEN_WIDTH - GameState.TEMP_EDITOR_WIDTH, GameState.TEMP_SCREEN_HEIGHT)
        else:
            self.board_screen_rect = pg.Rect(0, 0, GameState.TEMP_SCREEN_WIDTH, GameState.TEMP_SCREEN_HEIGHT)
            #TODO: move the person to somewhere safe
        self.person.set_start_pos()
        self.reset()
        self.board.set_screen_rect(self.board_screen_rect)

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

    def reset(self):
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

    def update_state(self):
        self.resolve_goals()
        self.move_character(self.person)
        for smick in self.smicks.values():
            if smick.is_alive:
                self.move_character(smick)
        self.resolve_deaths()

    def resolve_deaths(self):
        for smick in self.smicks.values():
            if smick.is_alive and smick.pos == self.person.pos:
                self.person.kill()

    def resolve_goals(self):
        coin = self.coins.get(self.person.pos)
        if coin is not None and coin.is_available:
            coin.is_available = False
            self.set_available_coin_count(self.available_coin_count - 1)