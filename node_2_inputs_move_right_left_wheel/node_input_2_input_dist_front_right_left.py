__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import pygame
from Vec2D import Vec2d


class NodeInputs(BaseNodeInputs):

	def __init__(self):
		super().__init__(2)

		# set the min max for the two input
		self.min_max_inputs[0][0] = 0
		self.min_max_inputs[0][1] = 100
		self.min_max_inputs[1][0] = 0
		self.min_max_inputs[1][1] = 100

		self.distance_left = 50
		self.distance_right = 50

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(self.nb_inputs)

		# fill the fragment with the inputs from the node
		current_fragment.input_array[0] = self.distance_left
		current_fragment.input_array[1] = self.distance_right

		return current_fragment

	def update(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_r]:
			self.distance_left = 0 if self.distance_left - 0.1 < 0 else self.distance_left - 0.1
		elif pressed[pygame.K_t]:
			self.distance_left = 100 if self.distance_left + 0.1 > 100 else self.distance_left + 0.1

		if pressed[pygame.K_f]:
			self.distance_right = 0 if self.distance_right - 0.1 < 0 else self.distance_right - 0.1
		elif pressed[pygame.K_g]:
			self.distance_right = 100 if self.distance_right + 0.1 > 100 else self.distance_right + 0.1

	def draw(self, pygame_draw, window):
		integer_pos = Vec2d(int(self.node.pos.x), int(self.node.pos.y))
		right_dir = Vec2d(self.node.dir)
		right_dir.rotate(10.0)
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + right_dir * self.distance_right + window.get_rect().center)

		left_dir = Vec2d(self.node.dir)
		left_dir.rotate(-10.0)
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + left_dir * self.distance_left + window.get_rect().center)
