from blocks import PipeBlock, EmptyBlock
import pygame as pg
import colors
from point import *

class Pipe:

    PIPE_CAP_HEIGHT_PERCENTAGE = .25
    PIPE_CAP_WIDTH_PERCENTAGE = .9
    ANCHOR_HEIGHT_PERCENTAGE = .25
    ANCHOR_WIDTH_PERCENTAGE = .12
    ANCHOR_COLOR = colors.GREY

    def __init__(self, board, top_pos, bottom_pos):
        self.board = board
        self.top_pos = top_pos
        self.bottom_pos = bottom_pos

        self.max_top_pos = top_pos
        self.min_bottom_pos = self._find_min_bottom_pos()

        self.anchor_pos = self.bottom_pos

        self.color = board.get_block(self.top_pos).color

    def _find_min_bottom_pos(self):
        length = self.top_pos.y - self.bottom_pos.y + 1
        cur_pos = self.bottom_pos
        for _ in range(1, length):
            cur_pos = point_down(cur_pos)
            cur_block = self.board.get_block(cur_pos)
            if not isinstance(cur_block, EmptyBlock):
                return point_up(cur_pos)

        return cur_pos

    def can_move_down(self):
        return self.bottom_pos.y > self.min_bottom_pos.y

    def can_move_up(self):
        return self.top_pos.y < self.max_top_pos.y

    def move(self, down=True):
        if down:
            self.move_down()
        else:
            self.move_up()

    def move_up(self):
        if self.can_move_up():
            self.top_pos = point_up(self.top_pos)
            self.board.swap_blocks(self.top_pos, self.bottom_pos)
            self.bottom_pos = point_up(self.bottom_pos)

    def move_down(self):
        if self.can_move_down():
            self.bottom_pos = point_down(self.bottom_pos)
            self.board.swap_blocks(self.top_pos, self.bottom_pos)
            self.top_pos = point_down(self.top_pos)

    def render(self, screen):
        self._render_top_cap(screen)
        self._render_bottom_cap(screen)
        self._render_anchor(screen)

    def _set_cap_left_width(self, rect):
        new_width = rect.width * Pipe.PIPE_CAP_WIDTH_PERCENTAGE
        rect.left += (rect.width - new_width) / 2
        rect.width = new_width

    def _render_top_cap(self, screen):
        top_rect = self.board.get_render_rect(self.top_pos)
        top_rect.height *= Pipe.PIPE_CAP_HEIGHT_PERCENTAGE
        self._set_cap_left_width(top_rect)
        pg.draw.rect(screen, self.color, top_rect)

    def _render_bottom_cap(self, screen):
        bottom_rect = self.board.get_render_rect(self.bottom_pos)
        new_height = bottom_rect.height * Pipe.PIPE_CAP_HEIGHT_PERCENTAGE
        bottom_rect.top += (bottom_rect.height - new_height) + 1
        bottom_rect.height = new_height
        self._set_cap_left_width(bottom_rect)
        pg.draw.rect(screen, self.color, bottom_rect)

    def _render_anchor(self, screen):
        anchor_rect = self.board.get_render_rect(self.anchor_pos)
        block_height = anchor_rect.height
        block_width = anchor_rect.width

        anchor_rect.height *= Pipe.ANCHOR_HEIGHT_PERCENTAGE
        anchor_rect.top += (1.5 * Pipe.ANCHOR_HEIGHT_PERCENTAGE * block_height)

        anchor_rect.width *= Pipe.ANCHOR_WIDTH_PERCENTAGE
        pg.draw.rect(screen, Pipe.ANCHOR_COLOR, anchor_rect)

        anchor_rect.left += (block_width - anchor_rect.width)
        pg.draw.rect(screen, Pipe.ANCHOR_COLOR, anchor_rect)


    def __repr__(self):
        return "top_pos:{} bottom_pos:{} max_top_pos:{} min_bottom_pos:{}".format(self.top_pos, self.bottom_pos, self.max_top_pos, self.min_bottom_pos)
