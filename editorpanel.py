import pygame as pg
from blocks import *
import colors

class EditorPanel:
    BORDER_WIDTH = 10
    SELECTOR_WIDTH = 3
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.index = 1
        self.blocks = [PipeBlock(colors.RED), PipeBlock(colors.BLUE), EmptyBlock(), RopeBlock(), GroundBlock()]

    def render(self, screen):
        pg.draw.rect(screen, colors.GREY, self.screen_rect)

        selection_height = self.screen_rect.height / len(self.blocks)

        rect = self.screen_rect.copy()
        rect.height = selection_height - EditorPanel.BORDER_WIDTH * 2
        rect.width -= EditorPanel.BORDER_WIDTH * 2
        rect.top += EditorPanel.BORDER_WIDTH
        rect.left += EditorPanel.BORDER_WIDTH

        for i in range(len(self.blocks)):
            block = self.blocks[i]
            pg.draw.rect(screen, colors.BLACK, rect)
            block.render(screen, rect)
            if self.index == i:
                pg.draw.rect(screen, colors.YELLOW, rect, EditorPanel.SELECTOR_WIDTH)

            rect.top += selection_height


