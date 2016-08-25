import pygame as pg
from blocks import *
import colors

class EditorPanel:
    BORDER_WIDTH = 10
    SELECTOR_WIDTH = 3
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.index = 0
        self.blocks = [PipeBlock(colors.RED), PipeBlock(colors.BLUE), EmptyBlock(), RopeBlock(), GroundBlock()]

    def handle_click(self, click_pos):
        for i in range(len(self.blocks)):
            if self._get_rect_for_index(i).collidepoint(click_pos):
                self.index = i
                return

    #TODO: almost all of this is the same for every call
    def _get_rect_for_index(self, index):
        selection_height = self.screen_rect.height / len(self.blocks)

        rect = self.screen_rect.copy()
        rect.height = selection_height - EditorPanel.BORDER_WIDTH * 2
        rect.width -= EditorPanel.BORDER_WIDTH * 2
        rect.left += EditorPanel.BORDER_WIDTH
        rect.top += EditorPanel.BORDER_WIDTH + selection_height * index
        return rect

    def get_selected_block(self):
        return self.blocks[self.index]

    def render(self, screen):
        pg.draw.rect(screen, colors.GREY, self.screen_rect)

        for i in range(len(self.blocks)):
            rect = self._get_rect_for_index(i)
            block = self.blocks[i]
            pg.draw.rect(screen, colors.BLACK, rect)
            block.render(screen, rect)
            if self.index == i:
                pg.draw.rect(screen, colors.YELLOW, rect, EditorPanel.SELECTOR_WIDTH)
