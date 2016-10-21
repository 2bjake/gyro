import pygame as pg
import colors

class Block:
    def __init__(self):
        self.is_solid = True

class EmptyBlock(Block):
    def __init__(self):
        self.is_solid = False

class DoorBlock(Block):
    def __init__(self):
        self.is_solid = True
        self.is_open = False

class GroundBlock(Block):
    def __init__(self):
        self.is_solid = True

class PipeBlock(Block):
    def __init__(self, color):
        self.color = color # TODO this should be a pipe color which translates to raw color
        self.is_solid = True

class RopeBlock(Block):
    def __init__(self):
        self.is_solid = False
