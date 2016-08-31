from blocks import PipeBlock, EmptyBlock
import pygame as pg
import colors
from collections import defaultdict


def create_pipes(board):
    pipes = defaultdict(list)

    x, y = 0, 0
    while x < board.matrix_rect.width:
        while y < board.matrix_rect.height:
            block = board.get_block(x, y)
            if isinstance(block, PipeBlock):
                pipe, y = create_pipe(board, x, y, block.color)
                pipes[block.color].append(pipe)
            y += 1
        x += 1
        y = 0
    return pipes

def create_pipe(board, bottom_x, bottom_y, color):
    cur_y = bottom_y
    cur_block = board.get_block(bottom_x, cur_y)
    while isinstance(cur_block, PipeBlock) and cur_block.color == color:
        cur_y += 1
        cur_block = board.get_block(bottom_x, cur_y)
    top_y = cur_y - 1

    return Pipe(board, bottom_x, top_y, bottom_y), top_y

class Pipe:

    PIPE_CAP_HEIGHT_PERCENTAGE = .25
    PIPE_CAP_WIDTH_PERCENTAGE = .9
    ANCHOR_HEIGHT_PERCENTAGE = .25
    ANCHOR_WIDTH_PERCENTAGE = .12
    ANCHOR_COLOR = colors.GREY

    def __init__(self, board, x, top_y, bottom_y):
        self.board = board
        self.x = x
        self.top_y = top_y
        self.max_top_y = top_y

        self.bottom_y = bottom_y
        self.min_bottom_y = self._find_min_bottom_y()

        self.anchor_y = bottom_y

        self.color = board.get_block(x, top_y).color

    def _find_min_bottom_y(self):
        length = self.top_y - self.bottom_y + 1

        for i in range(1, length):
            cur_y = self.bottom_y - i
            cur_block = self.board.get_block(self.x, cur_y)
            if not isinstance(cur_block, EmptyBlock):
                return cur_y + 1

        return self.bottom_y - length + 1

    def can_move_down(self):
        return self.bottom_y > self.min_bottom_y

    def can_move_up(self):
        return self.top_y < self.max_top_y

    def move(self, down=True):
        if down:
            self.move_down()
        else:
            self.move_up()

    def move_up(self):
        if self.can_move_up():
            self.top_y += 1
            self.board.swap_blocks(self.x, self.top_y, self.x, self.bottom_y)
            self.bottom_y += 1

    def move_down(self):
        if self.can_move_down():
            self.bottom_y -= 1
            self.board.swap_blocks(self.x, self.top_y, self.x, self.bottom_y)
            self.top_y -= 1

    def render(self, screen):
        self._render_top_cap(screen)
        self._render_bottom_cap(screen)
        self._render_anchor(screen)

    def _set_cap_left_width(self, rect):
        new_width = rect.width * Pipe.PIPE_CAP_WIDTH_PERCENTAGE
        rect.left += (rect.width - new_width) / 2
        rect.width = new_width

    def _render_top_cap(self, screen):
        top_rect = self.board.get_render_rect(self.x, self.top_y)
        top_rect.height *= Pipe.PIPE_CAP_HEIGHT_PERCENTAGE
        self._set_cap_left_width(top_rect)
        pg.draw.rect(screen, self.color, top_rect)

    def _render_bottom_cap(self, screen):
        bottom_rect = self.board.get_render_rect(self.x, self.bottom_y)
        new_height = bottom_rect.height * Pipe.PIPE_CAP_HEIGHT_PERCENTAGE
        bottom_rect.top += (bottom_rect.height - new_height) + 1
        bottom_rect.height = new_height
        self._set_cap_left_width(bottom_rect)
        pg.draw.rect(screen, self.color, bottom_rect)

    def _render_anchor(self, screen):
        anchor_rect = self.board.get_render_rect(self.x, self.anchor_y)
        block_height = anchor_rect.height
        block_width = anchor_rect.width

        anchor_rect.height *= Pipe.ANCHOR_HEIGHT_PERCENTAGE
        anchor_rect.top += (1.5 * Pipe.ANCHOR_HEIGHT_PERCENTAGE * block_height)

        anchor_rect.width *= Pipe.ANCHOR_WIDTH_PERCENTAGE
        pg.draw.rect(screen, Pipe.ANCHOR_COLOR, anchor_rect)

        anchor_rect.left += (block_width - anchor_rect.width)
        pg.draw.rect(screen, Pipe.ANCHOR_COLOR, anchor_rect)


    def __repr__(self):
        return "x:{} top_y:{} bottom_y:{} max_top_y:{} min_bottom_y:{}".format(self.x, self.top_y, self.bottom_y, self.max_top_y, self.min_bottom_y)
