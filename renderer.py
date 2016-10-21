import pygame as pg
from characters import *
from board import *
from pipe import *
from blocks import *
import colors

class Renderer:
    EDITOR_WIDTH = 80

    def __init__(self, screen, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = screen

        self._editor_screen_rect = pg.Rect(0, 0, Renderer.EDITOR_WIDTH, screen_height)
        self._board_no_editor_screen_rect = pg.Rect(0, 0, screen_width, screen_height)
        self._board_with_editor_screen_rect = pg.Rect(Renderer.EDITOR_WIDTH, 0, screen_width - Renderer.EDITOR_WIDTH, screen_height)

        self._character_renderer = CharacterRenderer(self._screen)
        self._pipe_renderer = PipeRenderer(self._screen)
        self._coin_renderer = CoinRenderer(self._screen)
        self._block_renderer = BlockRenderer(self._screen)
        self._board_renderer = BoardRenderer(self._screen, self._block_renderer)
        self._editor_renderer = EditorRenderer(self._screen, self._block_renderer)

    def _get_board_screen_rect(self, editor_enabled):
        if editor_enabled:
            return self._board_with_editor_screen_rect
        else:
            return self._board_no_editor_screen_rect

    def render(self, game_state):
        self._screen.fill(colors.BLACK)
        board_rect = self._get_board_screen_rect(game_state.editor_enabled)
        self._board_renderer.render(game_state.board, board_rect)
        self._render_visible_pipes(game_state)

        self._character_renderer.render_smicks(game_state.smicks.values())
        self._character_renderer.render_person(game_state.person)
        

        for coin in game_state.coins.values():
            coin_rect = game_state.board.get_render_rect(coin.pos)
            self._coin_renderer.render(coin, coin_rect)

        if game_state.editor_enabled:
            self._editor_renderer.render(game_state.editor, self._editor_screen_rect)

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
    PERSON_SCALE = 1.0/4
    SMICK_COLOR = colors.GREEN
    SMICK_SCALE = 1.0/3

    def __init__(self, screen):
        self._screen = screen

    def render_person(self, person):
        self._render_character(person, CharacterRenderer.PERSON_COLOR, CharacterRenderer.PERSON_SCALE)

    def render_smicks(self, smicks):
        for smick in smicks:
            self._render_character(smick, CharacterRenderer.SMICK_COLOR, CharacterRenderer.SMICK_SCALE)

    def _render_character(self, character, color, scale):
        if character.is_alive:
            rect = character.board.get_render_rect(character.pos)
            pg.draw.circle(self._screen, color, rect.center, int(rect.width * scale))

class CoinRenderer:
    COIN_COLOR = colors.YELLOW

    def __init__(self, screen):
        self._screen = screen

    def render(self, coin, rect):
        if coin.is_available:            
            pg.draw.circle(self._screen, CoinRenderer.COIN_COLOR, rect.center, rect.width / 8)

class BoardRenderer:
    def __init__(self, screen, block_renderer):
        self._screen = screen
        self._block_renderer = block_renderer

    def render(self, board, rect):
        #render all blocks in view_port
        max_x = min(board.matrix_rect.right, board.view_rect.right) #might not be necessary, make adjust_view_port always have view_rect right
        for x in range(board.view_rect.left, max_x):
            for y in range(board.matrix_rect.height):
                pos = Point(x, y)
                self._block_renderer.render_block(board.get_block(pos), board.get_render_rect(pos)) #TODO: use rect passed in


class BlockRenderer:
    def __init__(self, screen):
        self._screen = screen

    def render_block(self, block, rect):
        #block.render(self._screen, rect)
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

class EditorRenderer:
    BORDER_WIDTH = 10
    SELECTOR_WIDTH = 3

    def __init__(self, screen, block_renderer):
        self._screen = screen
        self._block_renderer = block_renderer

    #TODO: almost all of this is the same for every call
    def _get_block_rect_for_index(self, block_index, total_blocks, editor_rect):
        selection_height = editor_rect.height / total_blocks

        block_rect = editor_rect.copy()
        block_rect.height = selection_height - EditorRenderer.BORDER_WIDTH * 2
        block_rect.width -= EditorRenderer.BORDER_WIDTH * 2
        block_rect.left += EditorRenderer.BORDER_WIDTH
        block_rect.top += EditorRenderer.BORDER_WIDTH + selection_height * block_index
        return block_rect

    def render(self, editor, rect):
        pg.draw.rect(self._screen, colors.GREY, rect)
        total_blocks = len(editor.blocks)
        for i in range(total_blocks):
            block_rect = self._get_block_rect_for_index(i, total_blocks, rect)
            block = editor.blocks[i]
            pg.draw.rect(self._screen, colors.BLACK, block_rect)
            self._block_renderer.render_block(block, block_rect)
            if editor.index == i:
                pg.draw.rect(self._screen, colors.YELLOW, block_rect, EditorRenderer.SELECTOR_WIDTH)

