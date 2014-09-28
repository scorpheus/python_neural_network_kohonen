__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import copy
from simple_vec2d import SimpleVec2D


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

	def update(self, physic_world):
		left_dir = copy.copy(self.node.dir)
		left_dir.rotate(-10.0)
		self.distance_left = max(0, min(100, physic_world.intersection_line_spheres(self.node.pos, left_dir, 100)))

		right_dir = copy.copy(self.node.dir)
		right_dir.rotate(10.0)
		self.distance_right = max(0, min(100, physic_world.intersection_line_spheres(self.node.pos, right_dir, 100)))

	def draw(self, pygame_draw, window):
		integer_pos = SimpleVec2D(int(self.node.pos.x), int(self.node.pos.y))
		left_dir = copy.copy(self.node.dir)
		left_dir.rotate(-10.0)
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + left_dir * self.distance_left + window.get_rect().center)

		right_dir = copy.copy(self.node.dir)
		right_dir.rotate(10.0)
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + right_dir * self.distance_right + window.get_rect().center)

