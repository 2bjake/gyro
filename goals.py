import colors
import pygame as pg
from point import Point

class Coin:
    def __init__(self, board, pos):
        print(pos)
        self.board = board
        self.pos = pos
        self.color = colors.YELLOW
        self.reset()

    def reset(self):
        self.is_available = True

    def render(self, screen):
        if self.is_available:
            rect = self.board.get_render_rect(self.pos)
            pg.draw.circle(screen, self.color, rect.center, rect.width / 8)