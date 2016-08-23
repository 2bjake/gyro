import blocks
import colors
import pygame as pg

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_matrix = [[blocks.Block() for y in range(height)] for x in range(width)]

    def render(self, screen, block_size):
        for x in range(self.width):
            for y in range(self.height):
                self._render_block(screen, x, y, block_size)

    def _render_block(self, screen, block_x, block_y, block_size):
        rect = ((block_size * block_x, block_size * (self.height - block_y - 1)), (block_size, block_size));
        self.block_matrix[block_x][block_y].render(screen, rect)

    def set_block(self, x, y, block):
        self.block_matrix[x][y] = block

#    def get_block(self, x, y):
#        return self self.block_natrix[x][y]
