import colors
import pygame as pg

class Coin:
    def __init__(self, board, (x, y)):
        self.board = board
        self.x = x
        self.y = y
        self.color = colors.YELLOW
        self.reset()

    def reset(self):
        self.is_available = True

    def render(self, screen):
        if self.is_available:
            rect = self.board.get_render_rect(self.x, self.y)
            pg.draw.circle(screen, self.color, rect.center, rect.width / 8)