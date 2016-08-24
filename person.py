import colors
import pygame as pg
import blocks

class Person:
	def __init__(self, board, x, y):
		self.board = board
		self.initial_x = x
		self.initial_y = y
		self.reset()

	def can_move(self, new_x, new_y):
		dest_block = self.board.get_block(new_x, new_y)
		return isinstance(dest_block, blocks.EmptyBlock) or isinstance(dest_block, blocks.RopeBlock)

	def move_left(self):
		self.move(self.x - 1, self.y)

	def move_right(self):
		self.move(self.x + 1, self.y)

	def move_up(self):
		self.move(self.x, self.y + 1)

	def move_down(self):
		self.move(self.x, self.y - 1)

	def move(self, new_x, new_y):
		if self.dead:
			self.reset()
		elif self.can_move(new_x, new_y):
			self.x = new_x
			self.y = new_y

	def kill(self):
		self.dead = True

	def reset(self):
		self.dead = False
		self.x = self.initial_x
		self.y = self.initial_y

	def render(self, screen, block_size):
		if not self.dead:
			rect = self.board.get_render_rect(self.x, self.y, block_size)
			center_x = rect.left + block_size / 2
			center_y = rect.top + block_size / 2
			pg.draw.circle(screen, colors.PINK, (center_x, center_y), block_size / 4)