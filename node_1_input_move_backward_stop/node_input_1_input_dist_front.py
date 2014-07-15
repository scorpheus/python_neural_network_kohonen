__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import pygame
from Vec2D import Vec2d


class NodeInputs(BaseNodeInputs):

	def __init__(self):
		super().__init__(1)

		# set the min max for the first input
		self.min_max_inputs[0][0] = 0
		self.min_max_inputs[0][1] = 100

		self.distance_front = 50

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(self.nb_inputs)

		# fill the fragment with the inputs from the node
		current_fragment.input_array[0] = self.distance_front

		return current_fragment

	def update(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_r]:
			self.distance_front = 0 if self.distance_front - 0.1 < 0 else self.distance_front - 0.1
		elif pressed[pygame.K_t]:
			self.distance_front = 100 if self.distance_front + 0.1 > 100 else self.distance_front + 0.1

	def draw(self, pygame_draw, window):
		integer_pos = Vec2d(int(self.node.pos.x), int(self.node.pos.y))
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + self.node.dir * self.distance_front + window.get_rect().center)
