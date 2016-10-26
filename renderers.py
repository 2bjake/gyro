import pygame as pg
import colors
from blocks import *

class CharacterRenderer:
    PERSON_COLOR = colors.PINK
    PERSON_SCALE = 1/4.0
    SMICK_COLOR = colors.GREEN
    SMICK_SCALE = 1/3.0

    def __init__(self, screen):
        self._screen = screen

    def render_person(self, person, render_rect):
        self._render_character(person, render_rect, CharacterRenderer.PERSON_COLOR, CharacterRenderer.PERSON_SCALE)

    def render_smick(self, smick, render_rect):
        self._render_character(smick, render_rect, CharacterRenderer.SMICK_COLOR, CharacterRenderer.SMICK_SCALE)

    def _render_character(self, character, render_rect, color, scale):
        if character.is_alive:
            pg.draw.circle(self._screen, color, render_rect.center, int(render_rect.width * scale))

class CoinRenderer:
    COIN_COLOR = colors.YELLOW

    def __init__(self, screen):
        self._screen = screen

    def render(self, coin, rect):
        if coin.is_available:
            pg.draw.circle(self._screen, CoinRenderer.COIN_COLOR, rect.center, rect.width / 8)

class BlockRenderer:
    def __init__(self, screen):
        self._screen = screen

    def render_block(self, block, rect):
        if isinstance(block, EmptyBlock):
            pass # nothing to do
        elif isinstance(block, DoorBlock):
            self._render_door_block(block, rect)
        elif isinstance(block, GroundBlock):
            self._render_ground_block(block, rect)
        elif isinstance(block, PipeBlock):
            self._render_pipe_block(block, rect)
        elif isinstance(block, RopeBlock):
            self._render_rope_block(block, rect)
        else:
            pg.draw.rect(self._screen, colors.PINK, rect) # ugly to show something is wrong

    DOOR_WIDTH_PERCENTAGE = .7
    DOOR_CRACK_WIDTH = 3

    def _render_door_block(self, block, rect):
        door_rect = rect.copy()
        door_rect.width = door_rect.width * BlockRenderer.DOOR_WIDTH_PERCENTAGE
        door_rect.left += (rect.width - door_rect.width) / 2
        if not block.is_open:
            pg.draw.rect(self._screen, colors.ORANGE, door_rect)
            pg.draw.line(self._screen, colors.BLACK, rect.midtop, rect.midbottom, BlockRenderer.DOOR_CRACK_WIDTH)
        else:
            pass #draw open door

    GROUND_HEIGHT_PERCENTAGE = .125
    GROUND_MID_LINE_WIDTH = 5
    GROUND_COLOR = colors.WHITE

    def _render_ground_block(self, block, rect):
        top_rect = rect.copy()
        top_rect.height *= BlockRenderer.GROUND_HEIGHT_PERCENTAGE
        pg.draw.rect(self._screen, BlockRenderer.GROUND_COLOR, top_rect)

        start_pos = (rect.left, rect.top + BlockRenderer.GROUND_MID_LINE_WIDTH)
        end_pos = (rect.right, rect.bottom - BlockRenderer.GROUND_MID_LINE_WIDTH)
        pg.draw.line(self._screen, BlockRenderer.GROUND_COLOR, start_pos, end_pos, BlockRenderer.GROUND_MID_LINE_WIDTH)

        bottom_rect = rect.copy()
        bottom_rect.height *= BlockRenderer.GROUND_HEIGHT_PERCENTAGE
        bottom_rect.top = rect.bottom - bottom_rect.height - 1
        pg.draw.rect(self._screen, BlockRenderer.GROUND_COLOR, bottom_rect)

    PIPE_WIDTH_PERCENTAGE = .7

    def _render_pipe_block(self, block, rect):
        pipe_rect = rect.copy()
        pipe_rect.width = pipe_rect.width * BlockRenderer.PIPE_WIDTH_PERCENTAGE
        pipe_rect.left += (rect.width - pipe_rect.width) / 2
        pg.draw.rect(self._screen, block.color, pipe_rect)

    ROPE_WIDTH = 3

    def _render_rope_block(self, block, rect):
        pg.draw.line(self._screen, colors.BROWN, rect.midtop, rect.midbottom, BlockRenderer.ROPE_WIDTH)

class PipeRenderer:
    CAP_HEIGHT_PERCENTAGE = .25
    CAP_WIDTH_PERCENTAGE = .9
    ANCHOR_HEIGHT_PERCENTAGE = .25
    ANCHOR_WIDTH_PERCENTAGE = .12
    ANCHOR_COLOR = colors.GREY

    def __init__(self, screen):
        self._screen = screen

    def render_details(self, pipe, top_render_rect, bottom_render_rect, anchor_render_rect):
        self._render_top_cap(pipe, top_render_rect)
        self._render_bottom_cap(pipe, bottom_render_rect)
        self._render_anchor(pipe, anchor_render_rect)

    def _make_cap_rect(self, rect):
        new_width = rect.width * PipeRenderer.CAP_WIDTH_PERCENTAGE
        rect.left += (rect.width - new_width) / 2
        rect.width = new_width
        return rect

    def _render_top_cap(self, pipe, top_rect):
        top_rect = self._make_cap_rect(top_rect)
        top_rect.height *= PipeRenderer.CAP_HEIGHT_PERCENTAGE

        pg.draw.rect(self._screen, pipe.color, top_rect)

    def _render_bottom_cap(self, pipe, bottom_rect):
        bottom_rect = self._make_cap_rect(bottom_rect)
        new_height = bottom_rect.height * PipeRenderer.CAP_HEIGHT_PERCENTAGE
        bottom_rect.top += (bottom_rect.height - new_height) + 1
        bottom_rect.height = new_height

        pg.draw.rect(self._screen, pipe.color, bottom_rect)

    def _render_anchor(self, pipe, anchor_rect):
        block_height = anchor_rect.height
        block_width = anchor_rect.width

        anchor_rect.height *= PipeRenderer.ANCHOR_HEIGHT_PERCENTAGE
        anchor_rect.top += (1.5 * PipeRenderer.ANCHOR_HEIGHT_PERCENTAGE * block_height)

        anchor_rect.width *= PipeRenderer.ANCHOR_WIDTH_PERCENTAGE
        pg.draw.rect(self._screen, PipeRenderer.ANCHOR_COLOR, anchor_rect)

        anchor_rect.left += (block_width - anchor_rect.width)
        pg.draw.rect(self._screen, PipeRenderer.ANCHOR_COLOR, anchor_rect)
