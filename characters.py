import colors
import pygame as pg
import blocks

class Character(object):
    def __init__(self, board, (start_x, start_y)):
        self.board = board
        self.start_x = start_x
        self.start_y = start_y
        self.reset()
        self.color = colors.WHITE
        self.can_reset = False

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
        if self.is_dead and self.can_reset:
            self.reset()
        elif self.can_move(new_x, new_y) or (force and self.board.is_inside_border(new_x, new_y)):
            self.x, self.y = new_x, new_y

    def kill(self):
        self.is_dead = True

    def reset(self):
        self.is_dead = False
        self.x = self.start_x
        self.y = self.start_y

    def render(self, screen):
        if not self.is_dead:
            rect = self.board.get_render_rect(self.x, self.y)
            pg.draw.circle(screen, self.color, rect.center, rect.width / 4)


class Person(Character):
    def __init__(self, board, (start_x, start_y)):
        super(Person, self).__init__(board, (start_x, start_y))
        self.color = colors.PINK
        self.can_reset = True

class Smick(Character):
    def __init__(self, board, (start_x, start_y)):
        super(Smick, self).__init__(board, (start_x, start_y))
        self.color = colors.GREEN
