import colors
import pygame as pg
from point import Point

class Coin:
    def __init__(self, pos):
        print(pos)
        self.pos = pos
        self.reset()

    def reset(self):
        self.is_available = True
