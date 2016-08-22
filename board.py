import blocks
import pygame as pg

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blockMatrix = [[blocks.Block() for y in range(height)] for x in range(width)]
        self.blockMatrix[0][0] = blocks.GroundBlock()
        self.blockMatrix[width - 1][height - 1] = blocks.EmptyBlock()

    def render(self, screen, block_size):
        for x in range(self.width):
            for y in range(self.height):
                self._render_block(screen, x, y, block_size)

    def _render_block(self, screen, block_x, block_y, block_size):
        rect = ((block_size * block_x, block_size * (self.height - block_y - 1)), (block_size, block_size));
        self.blockMatrix[block_x][block_y].render(screen, rect)
