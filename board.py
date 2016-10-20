from blocks import *
import colors
import pygame as pg
from pipe import Pipe

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

    def get_render_rect(self, x, y):
        screen_x, screen_y = self.matrix_coords_to_screen_coords(x, y)
        return pg.Rect(screen_x, screen_y, self.block_size, self.block_size)

    def matrix_coords_to_screen_coords(self, matrix_x, matrix_y):
        x = self.screen_rect.x + self.block_size * (matrix_x - self.view_rect.left)
        y = self.screen_rect.top + self.block_size * (self.matrix_rect.height - matrix_y - 1)
        return x, y

    def screen_coords_to_matrix_coords(self, screen_x, screen_y):
        x = (screen_x - self.screen_rect.x)/ self.block_size + self.view_rect.left
        y = self.matrix_rect.height - screen_y / self.block_size - 1 + self.screen_rect.y
        return x, y

    def is_inside_border(self, x, y):
        return (self.matrix_rect.left < x < self.matrix_rect.right - 2 and
                self.matrix_rect.top < y < self.matrix_rect.bottom - 1)


    def add_block_at(self, (click_x, click_y), block):
        x, y = self.screen_coords_to_matrix_coords(click_x, click_y)
        if self.is_inside_border(x, y):
            self._set_block(x, y, block)
            return True
        return False

    def render(self, screen):
        #render all blocks in view_port
        max_x = min(self.matrix_rect.right, self.view_rect.right) #might not be necessary, make adjust_view_port always have view_rect right
        for x in range(self.view_rect.left, max_x):
            for y in range(self.matrix_rect.height):
                self._render_block(screen, x, y)

    def _render_block(self, screen, block_x, block_y):
        rect = self.get_render_rect(block_x, block_y)
        self.get_block(block_x, block_y).render(screen, rect)

    def _set_block(self, x, y, block):
        self.block_matrix[x][y] = block

    def swap_blocks(self, a_x, a_y, b_x, b_y):
        temp = self.get_block(a_x, a_y)
        self._set_block(a_x, a_y, self.get_block(b_x, b_y))
        self._set_block(b_x, b_y, temp)

    def get_block(self, x, y):
        return self.block_matrix[x][y]
