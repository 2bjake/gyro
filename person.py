import colors
import pygame as pg
import blocks

class Person:
	def __init__(self, board, x, y):
		self.board = board
		self.x = x
		self.y = y
		self.dead = False

	def can_move(self, new_x, new_y):
		dest_block = self.board.get_block(new_x, new_y)
		return isinstance(dest_block, blocks.EmptyBlock) or isinstance(dest_block, blocks.RopeBlock)

	def move_left(self):
		new_x = self.x - 1
		if not self.dead and self.can_move(new_x, self.y):
			self.x = new_x

	def move_right(self):
		new_x = self.x + 1
		if not self.dead and self.can_move(new_x, self.y):
			self.x = new_x

	def move_up(self):
		new_y = self.y + 1
		if not self.dead and self.can_move(self.x, new_y):
			self.y = new_y

	def move_down(self):
		new_y = self.y - 1
		if not self.dead and self.can_move(self.x, new_y):
			self.y = new_y

	def kill(self):
		self.dead = True

	def render(self, screen, block_size):
		if not self.dead:
			rect = self.board.get_render_rect(self.x, self.y, block_size)
			center_x = rect.left + block_size / 2
			center_y = rect.top + block_size / 2
			pg.draw.circle(screen, colors.PINK, (center_x, center_y), block_size / 4)