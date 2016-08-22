import pygame as pg
import colors

class Block:
    def __init__(self):
        self.color = colors.PINK

    def render(self, screen, rect):
        pg.draw.rect(screen, self.color, rect)

class EmptyBlock(Block):
    def __init__(self):
        self.color = colors.BLACK

class GroundBlock(Block):
    def __init__(self):
        self.color = colors.WHITE

class PipeBlock(Block):
    def __init__(self):
        # make this private/hidden or throw
        self.color = colors.PINK

    def __init__(self, color):
        self.color = color # TODO this should be a pipe color which translates to raw color