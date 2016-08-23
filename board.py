from blocks import PipeBlock
import colors
import pygame as pg
from collections import defaultdict
from pipe import Pipe

class Board:
    def __init__(self, block_matrix):
        self.width = len(block_matrix)
        self.height = len(block_matrix[0])
        self.block_matrix = block_matrix
        self._create_pipes()
        print self.pipes #remove me

    def render(self, screen, block_size):
        for x in range(self.width):
            for y in range(self.height):
                self._render_block(screen, x, y, block_size)

    def _render_block(self, screen, block_x, block_y, block_size):
        rect = ((block_size * block_x, block_size * (self.height - block_y - 1)), (block_size, block_size));
        self.block_matrix[block_x][block_y].render(screen, rect)

    def set_block(self, x, y, block):
        self.block_matrix[x][y] = block

    def get_block(self, x, y):
        return self.block_matrix[x][y]

    def _create_pipes(self):
        self.pipes = defaultdict(list)

        x, y = 0, 0
        while x < self.width:
            while y < self.height:
                block = self.block_matrix[x][y]
                if isinstance(block, PipeBlock):
                    (pipe, y) = self._create_pipe(x, y)
                    self.pipes[block.color].append(pipe)
                y += 1
            x += 1
            y = 0

    def _create_pipe(self, bottom_x, bottom_y):
        cur_y = bottom_y
        while isinstance(self.block_matrix[bottom_x][cur_y], PipeBlock): #BUG: when red pipe touches blue pipe
            cur_y += 1
        top_y = cur_y - 1

        return (Pipe(self, bottom_x, top_y, bottom_y), top_y)