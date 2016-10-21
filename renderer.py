import pygame as pg
from characters import *
from board import *
from pipe import *
from blocks import *
import colors

class Renderer:
	def __init__(self, screen, screen_width, screen_height):
		self._screen_width = screen_width
		self._screen_height = screen_height

		self._screen = screen

	def render(self, game_state):
		self._screen.fill(colors.BLACK)
		game_state.board.render(self._screen)
		self._render_pipes(game_state)
		game_state.person.render(self._screen)

		for smick in game_state.smicks.values():
			smick.render(self._screen)

		for coin in game_state.coins.values():
		    coin.render(self._screen)

		if game_state.editor_enabled:
		    game_state.editor.render(self._screen)

	def _render_pipes(self, game_state):
		#render pipe details
		#TODO: figure out the right way to do this without getting board internals
		# not sure i need to do this min, make adjust_view_port always make view_rect the right values
		# and then this code can just use it
		max_x = min(game_state.board.matrix_rect.right, game_state.board.view_rect.right)
		for color in game_state.pipes:
		    for pipe in game_state.pipes[color]:
		        if game_state.board.view_rect.left <= pipe.top_pos.x < max_x: # could use collidepoint
		            pipe.render(self._screen)


