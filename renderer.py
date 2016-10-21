import pygame as pg
from characters import *
from board import *
from pipe import *
from blocks import *
import colors

class Renderer:
    PERSON_COLOR = colors.PINK
    SMICK_COLOR = colors.GREEN

    def __init__(self, screen, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = screen

    def render(self, game_state):
        self._screen.fill(colors.BLACK)
        game_state.board.render(self._screen)
        self._render_pipes(game_state)
        self._render_person(game_state.board, game_state.person)
        self._render_smicks(game_state.board, game_state.smicks.values())

        for coin in game_state.coins.values():
            coin.render(self._screen)

        if game_state.editor_enabled:
            game_state.editor.render(self._screen)

    def _render_pipes(self, game_state):
        #TODO: figure out the right way to do this without getting board internals
        # not sure i need to do this min, make adjust_view_port always make view_rect the right values
        # and then this code can just use it
        max_x = min(game_state.board.matrix_rect.right, game_state.board.view_rect.right)
        for color in game_state.pipes:
            for pipe in game_state.pipes[color]:
                if game_state.board.view_rect.left <= pipe.top_pos.x < max_x: # could use collidepoint
                    pipe.render(self._screen)

    def _render_person(self, board, person):
        self._render_character(board, person, Renderer.PERSON_COLOR)

    def _render_smicks(self, board, smicks):
        for smick in smicks:
            self._render_character(board, smick, Renderer.SMICK_COLOR)

    def _render_character(self, board, character, color):
        if character.is_alive:
            rect = board.get_render_rect(character.pos)
            pg.draw.circle(self._screen, color, rect.center, rect.width / 4)


