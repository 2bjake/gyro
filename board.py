from blocks import *
from person import Person
import colors
import pygame as pg
from collections import defaultdict
from pipe import Pipe

class Board:
    DEFAULT_BLOCK_SIZE = 50

    def __init__(self, screen_rect, block_matrix, person_pos):
        self.width = len(block_matrix)
        self.height = len(block_matrix[0])

        self.block_size = Board.DEFAULT_BLOCK_SIZE

        self.view_x = 0
        self.set_screen_rect(screen_rect)

        self.block_matrix = block_matrix
        self._create_pipes()
        self.person = Person(self, person_pos)

    def set_screen_rect(self, rect):
        self.screen_rect = rect
        self.view_width = self.screen_rect.width / self.block_size

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
            self.view_x = max(0, self.person.x - 3)
        elif self.person.x < self.view_x + self.view_width / 3:
            self.view_x = max(0, self.person.x - 3)

    def get_render_rect(self, x, y):
        screen_x, screen_y = self.matrix_coords_to_screen_coords(x, y)
        return pg.Rect(screen_x, screen_y, self.block_size, self.block_size)

    def matrix_coords_to_screen_coords(self, matrix_x, matrix_y):
        x = self.screen_rect.x + self.block_size * (matrix_x - self.view_x)
        y = self.screen_rect.top + self.block_size * (self.height - matrix_y - 1)
        return x, y

    def screen_coords_to_matrix_coords(self, screen_x, screen_y):
        x = (screen_x - self.screen_rect.x)/ self.block_size + self.view_x
        y = self.height - screen_y / self.block_size - 1 + self.screen_rect.y
        return x, y

    def add_pipe_at(self, click_x, click_y, color):
        x, y = self.screen_coords_to_matrix_coords(click_x, click_y)

        self._set_block(x, y, PipeBlock(color))
        self._create_pipes()

    def render(self, screen):
        #render all blocks in view_port
        max_x = min(self.width, self.view_width + self.view_x)
        for x in range(self.view_x, max_x):
            for y in range(self.height):
                self._render_block(screen, x, y)

        self.person.render(screen)

        #render pipe details
        for key in self.pipes:
            for pipe in self.pipes[key]:
                if self.view_x <= pipe.x < max_x:
                    pipe.render(screen)

    def _render_block(self, screen, block_x, block_y):
        rect = self.get_render_rect(block_x, block_y)
        self.get_block(block_x, block_y).render(screen, rect)

    def _set_block(self, x, y, block):
        self.block_matrix[x][y] = block

    def swap_blocks(self, a_x, a_y, b_x, b_y):
        temp = self.get_block(a_x, a_y)
        self._set_block(a_x, a_y, self.get_block(b_x, b_y))
        self._set_block(b_x, b_y, temp)

    def get_block(self, x, y):
        return self.block_matrix[x][y]

    def _create_pipes(self):
        self.pipes = defaultdict(list)

        x, y = 0, 0
        while x < self.width:
            while y < self.height:
                block = self.get_block(x, y)
                if isinstance(block, PipeBlock):
                    (pipe, y) = self._create_pipe(x, y, block.color)
                    self.pipes[block.color].append(pipe)
                y += 1
            x += 1
            y = 0

    def _create_pipe(self, bottom_x, bottom_y, color): #BUG: if pipe is at top, this walks off the end
        cur_y = bottom_y
        cur_block = self.get_block(bottom_x, cur_y)
        while isinstance(cur_block, PipeBlock) and cur_block.color == color:
            cur_y += 1
            cur_block = self.get_block(bottom_x, cur_y)
        top_y = cur_y - 1

        return (Pipe(self, bottom_x, top_y, bottom_y), top_y)