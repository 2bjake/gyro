from blocks import *
import colors
import pygame as pg
from pipe import Pipe
from point import Point

class Board:
    DEFAULT_BLOCK_SIZE = 50

    def __init__(self, screen_rect, block_matrix):
        self.block_size = Board.DEFAULT_BLOCK_SIZE

        self.matrix_rect = pg.Rect(0, 0, len(block_matrix), len(block_matrix[0]))
        self.screen_rect = screen_rect
        self.view_rect = pg.Rect(0, 0, self.screen_rect.width / self.block_size, self.matrix_rect.height)

        self.block_matrix = block_matrix

    def set_screen_rect(self, rect):
        self.screen_rect = rect
        self.view_rect.width = self.screen_rect.width / self.block_size

    def adjust_view_port(self, x):
        forward_scroll_buffer = self.view_rect.width / 2
        backward_scroll_buffer = self.view_rect.width / 4
        end_x = min(self.view_rect.right, self.matrix_rect.right)
        if x > end_x - forward_scroll_buffer:
            self.view_rect.right = min(self.matrix_rect.right, x + forward_scroll_buffer)
        elif x < self.view_rect.left + backward_scroll_buffer:
            self.view_rect.left = max(0, x - backward_scroll_buffer)

    def get_render_rect(self, pos):
        screen_pos = self.matrix_coords_to_screen_coords(pos)
        return pg.Rect(screen_pos, (self.block_size, self.block_size))

    def matrix_coords_to_screen_coords(self, matrix_pos):
        x = self.screen_rect.x + self.block_size * (matrix_pos.x - self.view_rect.left)
        y = self.screen_rect.top + self.block_size * (self.matrix_rect.height - matrix_pos.y - 1)
        return Point(x, y)

    def screen_coords_to_matrix_coords(self, screen_pos):
        x = (screen_pos.x - self.screen_rect.x)/ self.block_size + self.view_rect.left
        y = self.matrix_rect.height - screen_pos.y / self.block_size - 1 + self.screen_rect.y
        return Point(x, y)

    def is_inside_border(self, pos):
        return (self.matrix_rect.left < pos.x < self.matrix_rect.right - 1 and
                self.matrix_rect.top < pos.y < self.matrix_rect.bottom - 1)

    #TODO: this method is weird, board shouldn't know about screen coords
    def add_block_at(self, click_pos, block):
        matrix_pos = self.screen_coords_to_matrix_coords(click_pos)
        if self.is_inside_border(matrix_pos):
            self._set_block(matrix_pos, block)
            return True
        return False

    def render(self, screen):
        #render all blocks in view_port
        max_x = min(self.matrix_rect.right, self.view_rect.right) #might not be necessary, make adjust_view_port always have view_rect right
        for x in range(self.view_rect.left, max_x):
            for y in range(self.matrix_rect.height):
                self._render_block(screen, Point(x, y))

    def _render_block(self, screen, pos):
        rect = self.get_render_rect(pos)
        self.get_block(pos).render(screen, rect)

    def _set_block(self, pos, block):
        self.block_matrix[pos.x][pos.y] = block

    def swap_blocks(self, a_pos, b_pos):
        temp = self.get_block(a_pos)
        self._set_block(a_pos, self.get_block(b_pos))
        self._set_block(b_pos, temp)

    def get_block(self, pos):
        return self.block_matrix[pos.x][pos.y]
