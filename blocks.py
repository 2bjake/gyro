import pygame as pg
import colors

GROUND_HEIGHT_PERCENTAGE = .25
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
    def __init__(self):
        self.color = colors.WHITE

    def render(self, screen, rect):
        top_rect = pg.Rect(rect)
        top_rect.height *= (1 - GROUND_HEIGHT_PERCENTAGE)
        pg.draw.rect(screen, BACKGROUND_COLOR, top_rect)

        bottom_rect = pg.Rect(rect)
        bottom_rect.top += top_rect.height
        bottom_rect.height *= GROUND_HEIGHT_PERCENTAGE
        pg.draw.rect(screen, self.color, bottom_rect)

class PipeBlock(Block):
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3

    PIPE_WIDTH_PERCENTAGE = .8

    def __init__(self, color):
        self.color = color # TODO this should be a pipe color which translates to raw color
        self.position = PipeBlock.MIDDLE

    def set_position(self, position):
        self.position = position

    def render(self, screen, rect):
        if self.position == PipeBlock.TOP:
            self.render_top(screen, rect)
        elif self.position == PipeBlock.MIDDLE:
            self.render_middle(screen, rect)
        else:
            self.render_bottom(screen, rect)

    def render_top(self, screen, rect):
        top_rect = pg.Rect(rect)
        top_rect.height *= (1 - GROUND_HEIGHT_PERCENTAGE)
        pg.draw.rect(screen, BACKGROUND_COLOR, top_rect)

        bottom_rect = pg.Rect(rect)
        bottom_rect.top += top_rect.height
        bottom_rect.height *= GROUND_HEIGHT_PERCENTAGE
        pg.draw.rect(screen, self.color, bottom_rect)

    def render_middle(self, screen, rect):
        pipe_rect = pg.Rect(rect)
        new_width = pipe_rect.width * PipeBlock.PIPE_WIDTH_PERCENTAGE
        pipe_rect.left += (pipe_rect.width - new_width) / 2
        pipe_rect.width = new_width
        pg.draw.rect(screen, self.color, pipe_rect)

    def render_bottom(self, screen, rect):
        top_rect = pg.Rect(rect)
        top_rect.height *= (1 - GROUND_HEIGHT_PERCENTAGE)
        pg.draw.rect(screen, BACKGROUND_COLOR, top_rect)

        bottom_rect = pg.Rect(rect)
        bottom_rect.top += top_rect.height
        bottom_rect.height *= GROUND_HEIGHT_PERCENTAGE
        pg.draw.rect(screen, self.color, bottom_rect)

        self.render_middle(screen, rect)
