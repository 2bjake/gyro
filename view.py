import pygame as pg
from renderers import *
from characters import *
from board import *
from pipe import *
from blocks import *
import colors

class View:
    EDITOR_WIDTH = 80
    BLOCK_SIZE = 50

    def __init__(self, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = pg.display.set_mode((screen_width, screen_height), 0, 32)
        pg.display.set_caption('GyroMine')

        self._editor_screen_rect = pg.Rect(0, 0, View.EDITOR_WIDTH, screen_height)
        self._board_no_editor_screen_rect = pg.Rect(0, 0, screen_width, screen_height)
        self._board_with_editor_screen_rect = pg.Rect(View.EDITOR_WIDTH, 0, screen_width - View.EDITOR_WIDTH, screen_height)

        self._board_view_rect = pg.Rect(0, 0, screen_width / View.BLOCK_SIZE, screen_height / View.BLOCK_SIZE)

        self._character_renderer = CharacterRenderer(self._screen)
        self._pipe_renderer = PipeRenderer(self._screen)
        self._coin_renderer = CoinRenderer(self._screen)
        self._block_renderer = BlockRenderer(self._screen)
        self._editor_renderer = EditorRenderer(self._screen, self._block_renderer)

    def _get_render_rect_for_board_position(self, pos, editor_enabled):
        screen_pos = self._get_screen_coords_for_board_position(pos, editor_enabled)
        return pg.Rect(screen_pos, (View.BLOCK_SIZE, View.BLOCK_SIZE))

    def _get_screen_coords_for_board_position(self, board_pos, editor_enabled):
        screen_rect = self.get_board_screen_rect(editor_enabled)

        x = screen_rect.x + View.BLOCK_SIZE * (board_pos.x - self._board_view_rect.left)
        y = screen_rect.top + View.BLOCK_SIZE * (self._board_view_rect.height - board_pos.y - 1)
        return Point(x, y)

    def get_board_screen_rect(self, editor_enabled):
        if editor_enabled:
            return self._board_with_editor_screen_rect
        else:
            return self._board_no_editor_screen_rect

    def get_editor_screen_rect(self):
        return self._editor_screen_rect

    def get_board_position_for_screen_position(self, screen_pos, editor_enabled):
        board_screen_rect = self.get_board_screen_rect(editor_enabled)
        x = (screen_pos.x - board_screen_rect.x) / View.BLOCK_SIZE + self._board_view_rect.left
        y = self._board_view_rect.height - screen_pos.y / View.BLOCK_SIZE - 1 + board_screen_rect.y
        return Point(x, y)

    def _get_in_view_board_rect(self, game_state):
        board_screen_rect = self.get_board_screen_rect(game_state.editor_enabled)
        board_view_width = board_screen_rect.width / View.BLOCK_SIZE
        board_view_height = board_screen_rect.height / View.BLOCK_SIZE

        board_view_rect = pg.Rect(0, 0, board_view_width, board_view_height)

        forward_scroll_buffer = board_view_width / 2
        board_view_rect.right = game_state.person.pos.x + forward_scroll_buffer
        if board_view_rect.right > game_state.board.rect.right:
            board_view_rect.right = game_state.board.rect.right

        if board_view_rect.left < 0:
            board_view_rect.left = 0

        return board_view_rect

    def render(self, game_state):
        self._board_view_rect = self._get_in_view_board_rect(game_state) #update in view rect based on game state

        self._screen.fill(colors.BLACK)
        self._render_board(game_state)
        self._render_pipes(game_state)

        # render smicks
        for smick in game_state.smicks.values():
            smick_rect = self._get_render_rect_for_board_position(smick.pos, game_state.editor_enabled)
            self._character_renderer.render_smick(smick, smick_rect)

        # render person
        person_rect = self._get_render_rect_for_board_position(game_state.person.pos, game_state.editor_enabled)
        self._character_renderer.render_person(game_state.person, person_rect)

        # render coins
        for coin in game_state.coins.values():
            coin_rect = self._get_render_rect_for_board_position(coin.pos, game_state.editor_enabled)
            self._coin_renderer.render(coin, coin_rect)

        # render editor
        if game_state.editor_enabled:
            self._editor_renderer.render(game_state.editor, self._editor_screen_rect)

    def _render_board(self, game_state):
        for x in range(self._board_view_rect.left, self._board_view_rect.right):
            for y in range(self._board_view_rect.height):
                pos = Point(x, y)
                block = game_state.board.get_block(pos)
                render_rect = self._get_render_rect_for_board_position(pos, game_state.editor_enabled)
                self._block_renderer.render_block(block, render_rect)

    def _render_pipes(self, game_state):
        for color in game_state.pipes:
            for pipe in game_state.pipes[color]:
                if self._board_view_rect.left <= pipe.top_pos.x < self._board_view_rect.right:
                    top_render_rect = self._get_render_rect_for_board_position(pipe.top_pos, game_state.editor_enabled)
                    bottom_render_rect = self._get_render_rect_for_board_position(pipe.bottom_pos, game_state.editor_enabled)
                    anchor_render_rect = self._get_render_rect_for_board_position(pipe.anchor_pos, game_state.editor_enabled)
                    self._pipe_renderer.render_details(pipe, top_render_rect, bottom_render_rect, anchor_render_rect)

