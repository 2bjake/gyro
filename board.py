from blocks import *
from person import Person
import colors
import pygame as pg
from collections import defaultdict
from pipe import Pipe

class Board:
    def __init__(self, block_matrix, person_x, person_y):
        self.width = len(block_matrix)
        self.height = len(block_matrix[0])

        self.view_x = 0
        self.view_width = self.width

        self.block_matrix = block_matrix
        self._create_pipes()
        self.person = Person(self, person_x, person_y)

    def move_pipes(self, color, down=True):
        if down:
            self.move_pipes_down(color)
        else:
            self.move_pipes_up(color)

    def move_pipes_down(self, color):
        for pipe in self.pipes[color]:
            pipe.move_down()

    def move_pipes_up(self, color):
        for pipe in self.pipes[color]:
            pipe.move_up()

    def resolve_collisions(self): #also handles falling which isn't really collisions...
        block_at_person = self.get_block(self.person.x, self.person.y)
        block_below_person = self.get_block(self.person.x, self.person.y - 1)

        if block_at_person.is_solid:
            if self.person.can_move(self.person.x, self.person.y + 1):
                self.person.move_up()
            else:
                self.person.kill()
        elif not block_below_person.is_solid and not isinstance(block_at_person, RopeBlock):
            self.person.move_down()

    def adjust_view_port(self):
        end_x = self.view_x + self.view_width
        if self.person.x > end_x - self.view_width / 3:
            self.view_x = self.person.x + 3
        elif self.person.x < self.view_x + self.view_width / 3:
            self.view_x = self.person.x - 3

    def get_render_rect(self, x, y, block_size):
        return pg.Rect((block_size * (x - self.view_x), block_size * (self.height - y - 1)), (block_size, block_size))

    #TODO: this is rendering elements that are out of the view_port
    def render(self, screen, block_size):
        #render all blocks
        for x in range(self.width):
            for y in range(self.height):
                self._render_block(screen, x, y, block_size)

        self.person.render(screen, block_size)

        #render pipe details
        for key in self.pipes:
            for pipe in self.pipes[key]:
                pipe.render(screen, block_size)

    def _render_block(self, screen, block_x, block_y, block_size):
        rect = self.get_render_rect(block_x, block_y, block_size)
        self.get_block(block_x, block_y).render(screen, rect)

    def set_block(self, x, y, block):
        self.block_matrix[x][y] = block

    def get_block(self, x, y):
        return self.block_matrix[x][y]

    def _create_pipes(self):
        self.pipes = defaultdict(list)

        x, y = 0, 0
        while x < self.width:
            while y < self.height:
                block = self.get_block(x, y)
                if isinstance(block, PipeBlock):
                    (pipe, y) = self._create_pipe(x, y)
                    self.pipes[block.color].append(pipe)
                y += 1
            x += 1
            y = 0

    def _create_pipe(self, bottom_x, bottom_y):
        cur_y = bottom_y
        while isinstance(self.get_block(bottom_x, cur_y), PipeBlock): #BUG: when red pipe touches blue pipe
            cur_y += 1
        top_y = cur_y - 1

        return (Pipe(self, bottom_x, top_y, bottom_y), top_y)