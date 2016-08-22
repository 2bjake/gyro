import pygame as pg
import colors

class Block:
    def __init__(self, color):
        self.color = color

    def render(self, screen, rect):
        pg.draw.rect(screen, self.color, rect)