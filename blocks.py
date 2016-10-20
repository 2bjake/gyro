import pygame as pg
import colors

class Block:
    def __init__(self):
        self.color = colors.PINK # something ugly to show that things are wrong
        self.is_solid = True

    def render(self, screen, rect):
        pg.draw.rect(screen, self.color, rect)

class EmptyBlock(Block):
    def __init__(self):
        self.is_solid = False

    def render(self, screen, rect):
        pass # nothing to draw

class DoorBlock(Block):
    DOOR_WIDTH_PERCENTAGE = .7
    DOOR_CRACK_WIDTH = 3

    def __init__(self):
        self.is_solid = True
        self.is_open = False
        self.color = colors.ORANGE

    def render(self, screen, rect):
        door_rect = rect.copy()
        door_rect.width = door_rect.width * DoorBlock.DOOR_WIDTH_PERCENTAGE
        door_rect.left += (rect.width - door_rect.width) / 2
        if not self.is_open:
            pg.draw.rect(screen, self.color, door_rect)
            pg.draw.line(screen, colors.BLACK, rect.midtop, rect.midbottom, DoorBlock.DOOR_CRACK_WIDTH)
        else:
            pass #draw open door

class GroundBlock(Block):
    GROUND_HEIGHT_PERCENTAGE = .125
    MID_LINE_WIDTH = 5

    def __init__(self):
        self.color = colors.WHITE
        self.is_solid = True

    def render(self, screen, rect):
        top_rect = rect.copy()
        top_rect.height *= GroundBlock.GROUND_HEIGHT_PERCENTAGE
        pg.draw.rect(screen, self.color, top_rect)

        start_pos = (rect.left, rect.top + GroundBlock.MID_LINE_WIDTH)
        end_pos = (rect.right, rect.bottom - GroundBlock.MID_LINE_WIDTH)
        pg.draw.line(screen, self.color, start_pos, end_pos, GroundBlock.MID_LINE_WIDTH)

        bottom_rect = rect.copy()
        bottom_rect.height *= GroundBlock.GROUND_HEIGHT_PERCENTAGE
        bottom_rect.top = rect.bottom - bottom_rect.height - 1
        pg.draw.rect(screen, self.color, bottom_rect)

class PipeBlock(Block):
    PIPE_WIDTH_PERCENTAGE = .7

    def __init__(self, color):
        self.color = color # TODO this should be a pipe color which translates to raw color
        self.is_solid = True

    def render(self, screen, rect):
        pipe_rect = rect.copy()
        pipe_rect.width = pipe_rect.width * PipeBlock.PIPE_WIDTH_PERCENTAGE
        pipe_rect.left += (rect.width - pipe_rect.width) / 2
        pg.draw.rect(screen, self.color, pipe_rect)

class RopeBlock(Block):
    WIDTH = 3

    def __init__(self):
        self.color = colors.BROWN
        self.is_solid = False

    def render(self, screen, rect):
        pg.draw.line(screen, self.color, rect.midtop, rect.midbottom, RopeBlock.WIDTH)
