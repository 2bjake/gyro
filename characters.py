import colors
import pygame as pg
import blocks
from point import *

class Character(object):
    def __init__(self, board, start_pos):
        self.board = board
        self.start_pos = start_pos
        self.reset()
        self.color = colors.WHITE
        self.can_reset = False

    def can_move(self, new_pos):
        dest_block = self.board.get_block(new_pos)
        return not dest_block.is_solid

    def move_left(self, force=False):
        self._move(point_left(self.pos), force)

    def move_right(self, force=False):
        self._move(point_right(self.pos), force)

    def move_up(self, force=False):
        self._move(point_up(self.pos), force)

    def move_down(self, force=False):
        self._move(point_down(self.pos), force)

    def _move(self, new_pos, force):
        if not self.is_alive and self.can_reset:
            self.reset()
        elif self.can_move(new_pos) or (force and self.board.is_inside_border(new_pos)):
            self.pos = new_pos

    def set_start_pos(self):
        self.start_pos = self.pos

    def kill(self):
        self.is_alive = False

    def reset(self):
        self.is_alive = True
        self.pos = self.start_pos

    def render(self, screen):
        if self.is_alive:
            rect = self.board.get_render_rect(self.pos)
            pg.draw.circle(screen, self.color, rect.center, rect.width / 4)


class Person(Character):
    def __init__(self, board, start_pos):
        super(Person, self).__init__(board, start_pos)
        self.color = colors.PINK
        self.can_reset = True

class Smick(Character):
    def __init__(self, board, start_pos):
        super(Smick, self).__init__(board, start_pos)
        self.color = colors.GREEN
