from blocks import PipeBlock, EmptyBlock
import pygame as pg
import colors
from point import *

class Pipe:
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

    def __repr__(self):
        return "top_pos:{} bottom_pos:{} max_top_pos:{} min_bottom_pos:{}".format(self.top_pos, self.bottom_pos, self.max_top_pos, self.min_bottom_pos)
