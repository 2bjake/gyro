import colors
import pygame as pg
import blocks

class Person:
    def __init__(self, board, (x, y)):
        self.board = board
        self.initial_x = x
        self.initial_y = y
        self.reset()

    def can_move(self, new_x, new_y):
        dest_block = self.board.get_block(new_x, new_y)
        return not dest_block.is_solid

    def move_left(self, force=False):
        self.move(self.x - 1, self.y, force)

    def move_right(self, force=False):
        self.move(self.x + 1, self.y, force)

    def move_up(self, force=False):
        self.move(self.x, self.y + 1, force)

    def move_down(self, force=False):
        self.move(self.x, self.y - 1, force)

    def move(self, new_x, new_y, force=False):
        if self.dead:
            self.reset()
        elif force or self.can_move(new_x, new_y):
            self.x, self.y = new_x, new_y

    def kill(self):
        self.dead = True

    def reset(self):
        self.dead = False
        self.x = self.initial_x
        self.y = self.initial_y

    def render(self, screen):
        if not self.dead:
            rect = self.board.get_render_rect(self.x, self.y)
            pg.draw.circle(screen, colors.PINK, rect.center, rect.width / 4)