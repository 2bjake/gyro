import pygame as pg
import colors

GROUND_HEIGHT_PERCENTAGE = .125
BACKGROUND_COLOR = colors.BLACK

class Block:
    def __init__(self):
        self.color = colors.PINK

    def render(self, screen, rect):
        pg.draw.rect(screen, self.color, rect)

class EmptyBlock(Block):
    def __init__(self):
        self.color = BACKGROUND_COLOR

class GroundBlock(Block):

    MIDDLE_GROUND_WIDTH_PERCENTAGE = 1
    MIDDLE_GROUND_HEIGHT_PERCENTAGE = .125

    def __init__(self):
        self.color = colors.WHITE

    def render(self, screen, rect):
        pg.draw.rect(screen, BACKGROUND_COLOR, rect)

        #TODO: this code is very similar to the pipe top/bottom code. Share it.
        top_rect = pg.Rect(rect)
        block_height = top_rect.height
        ground_height = block_height * GROUND_HEIGHT_PERCENTAGE

        top_rect.height = ground_height
        pg.draw.rect(screen, self.color, top_rect)

        start_pos = (top_rect.left, top_rect.top)
        end_pos = (top_rect.left + top_rect.width, top_rect.top + block_height - 5)
        pg.draw.line(screen, self.color, start_pos, end_pos, 5)

        bottom_rect = pg.Rect(rect)
        bottom_rect.height = ground_height
        bottom_rect.top += (block_height - ground_height)
        pg.draw.rect(screen, self.color, bottom_rect)

class PipeBlock(Block):
    PIPE_WIDTH_PERCENTAGE = .7

    def __init__(self, color):
        self.color = color # TODO this should be a pipe color which translates to raw color

    def render(self, screen, rect):
        self.render_background(screen, rect)
        self.render_middle(screen, rect)

    def render_background(self, screen, rect):
        pg.draw.rect(screen, BACKGROUND_COLOR, rect)

    def render_middle(self, screen, rect):
        pipe_rect = pg.Rect(rect)
        new_width = pipe_rect.width * PipeBlock.PIPE_WIDTH_PERCENTAGE
        pipe_rect.left += (pipe_rect.width - new_width) / 2
        pipe_rect.width = new_width
        pg.draw.rect(screen, self.color, pipe_rect)
