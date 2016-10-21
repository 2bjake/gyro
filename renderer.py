import pygame as pg
from characters import *
from board import *
from pipe import *
from blocks import *
import colors

class Renderer:

    def __init__(self, screen, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = screen
        self._character_renderer = CharacterRenderer(self._screen)
        self._pipe_renderer = PipeRenderer(self._screen)
        self._coin_renderer = CoinRenderer(self._screen)

    def render(self, game_state):
        self._screen.fill(colors.BLACK)
        game_state.board.render(self._screen)
        self._render_visible_pipes(game_state)

        self._character_renderer.render_person(game_state.person)
        self._character_renderer.render_smicks(game_state.smicks.values())

        for coin in game_state.coins.values():
            coin_rect = game_state.board.get_render_rect(coin.pos)
            self._coin_renderer.render(coin, coin_rect)

        if game_state.editor_enabled:
            game_state.editor.render(self._screen)

    def _render_visible_pipes(self, game_state):
        #TODO: figure out the right way to do this without getting board internals
        # not sure i need to do this min, make adjust_view_port always make view_rect the right values
        # and then this code can just use it
        max_x = min(game_state.board.matrix_rect.right, game_state.board.view_rect.right)
        for color in game_state.pipes:
            for pipe in game_state.pipes[color]:
                if game_state.board.view_rect.left <= pipe.top_pos.x < max_x: # could use collidepoint
                    self._pipe_renderer.render_details(pipe)

class CharacterRenderer:
    PERSON_COLOR = colors.PINK
    SMICK_COLOR = colors.GREEN

    def __init__(self, screen):
        self._screen = screen

    def render_person(self, person):
        self._render_character(person, CharacterRenderer.PERSON_COLOR)

    def render_smicks(self, smicks):
        for smick in smicks:
            self._render_character(smick, CharacterRenderer.SMICK_COLOR)

    def _render_character(self, character, color):
        if character.is_alive:
            rect = character.board.get_render_rect(character.pos)
            pg.draw.circle(self._screen, color, rect.center, rect.width / 4)

class CoinRenderer:
    COIN_COLOR = colors.YELLOW

    def __init__(self, screen):
        self._screen = screen

    def render(self, coin, rect):
        if coin.is_available:            
            pg.draw.circle(self._screen, CoinRenderer.COIN_COLOR, rect.center, rect.width / 8)

class PipeRenderer:
    CAP_HEIGHT_PERCENTAGE = .25
    CAP_WIDTH_PERCENTAGE = .9
    ANCHOR_HEIGHT_PERCENTAGE = .25
    ANCHOR_WIDTH_PERCENTAGE = .12
    ANCHOR_COLOR = colors.GREY

    def __init__(self, screen):
        self._screen = screen

    def render_details(self, pipe):
        self._render_top_cap(pipe)
        self._render_bottom_cap(pipe)
        self._render_anchor(pipe)

    def _make_cap_rect(self, rect):
        new_width = rect.width * PipeRenderer.CAP_WIDTH_PERCENTAGE
        rect.left += (rect.width - new_width) / 2
        rect.width = new_width
        return rect

    def _render_top_cap(self, pipe):
        top_rect = pipe.board.get_render_rect(pipe.top_pos)
        top_rect = self._make_cap_rect(top_rect)
        top_rect.height *= PipeRenderer.CAP_HEIGHT_PERCENTAGE

        pg.draw.rect(self._screen, pipe.color, top_rect)

    def _render_bottom_cap(self, pipe):
        bottom_rect = pipe.board.get_render_rect(pipe.bottom_pos)
        bottom_rect = self._make_cap_rect(bottom_rect)
        new_height = bottom_rect.height * PipeRenderer.CAP_HEIGHT_PERCENTAGE
        bottom_rect.top += (bottom_rect.height - new_height) + 1
        bottom_rect.height = new_height

        pg.draw.rect(self._screen, pipe.color, bottom_rect)

    def _render_anchor(self, pipe):
        anchor_rect = pipe.board.get_render_rect(pipe.anchor_pos)
        block_height = anchor_rect.height
        block_width = anchor_rect.width

        anchor_rect.height *= PipeRenderer.ANCHOR_HEIGHT_PERCENTAGE
        anchor_rect.top += (1.5 * PipeRenderer.ANCHOR_HEIGHT_PERCENTAGE * block_height)

        anchor_rect.width *= PipeRenderer.ANCHOR_WIDTH_PERCENTAGE
        pg.draw.rect(self._screen, PipeRenderer.ANCHOR_COLOR, anchor_rect)

        anchor_rect.left += (block_width - anchor_rect.width)
        pg.draw.rect(self._screen, PipeRenderer.ANCHOR_COLOR, anchor_rect)


