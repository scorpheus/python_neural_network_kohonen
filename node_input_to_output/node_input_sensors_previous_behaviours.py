__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import gs
import gs.plus.render as render
from vector_helper import rotate
import numpy as np


class NodeInputs(BaseNodeInputs):

	def __init__(self):
		self.previous_behaviours = np.zeros((50,))
		super().__init__(3 + len(self.previous_behaviours))

		# set the min max for the two input
		self.min_max_inputs[0][0] = 0
		self.min_max_inputs[0][1] = 4
		self.min_max_inputs[1][0] = 0
		self.min_max_inputs[1][1] = 4
		self.min_max_inputs[2][0] = 0
		self.min_max_inputs[2][1] = 2

		# add 5 previous action
		for i in range(3, 3 + len(self.previous_behaviours)):
			self.min_max_inputs[i][0] = 0
			self.min_max_inputs[i][1] = 3

		self.distance_left = 2.5
		self.distance_right = 2.5
		self.distance_back = 1

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(self.nb_inputs)

		# fill the fragment with the inputs from the node
		current_fragment.input_array[0] = self.distance_left
		current_fragment.input_array[1] = self.distance_right
		current_fragment.input_array[2] = self.distance_back

		for i in range(3, 3 + len(self.previous_behaviours)):
			current_fragment.input_array[i] = self.previous_behaviours[i-3]

		return current_fragment

	def update(self, physic_world):
		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		self.distance_left = max(0, min(4, physic_world.intersection_line_spheres(self.node.pos, left_dir, 4)))

		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		self.distance_right = max(0, min(4, physic_world.intersection_line_spheres(self.node.pos, right_dir, 4)))

		back_dir = gs.Vector2(self.node.dir) * -1
		self.distance_back = max(0, min(2, physic_world.intersection_line_spheres(self.node.pos, back_dir, 2)))

		# need 100 values not the intermediary, not necessary
		self.distance_left = int(self.distance_left * 100) / 100
		self.distance_right = int(self.distance_right * 100) / 100
		self.distance_back = int(self.distance_back * 100) / 100

		# roll the array and add to the current input
		self.previous_behaviours = np.roll(self.previous_behaviours, 1)
		self.previous_behaviours[0] = self.node.selected_action

	def draw(self):
		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		world_end_line = self.node.pos + left_dir * self.distance_left
		render.line3d(self.node.pos.x, 0, self.node.pos.y, world_end_line.x, 0, world_end_line.y)

		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		world_end_line = self.node.pos + right_dir * self.distance_right
		render.line3d(self.node.pos.x, 0, self.node.pos.y, world_end_line.x, 0, world_end_line.y)

		back_dir = gs.Vector2(self.node.dir) * -1
		world_end_line = self.node.pos + back_dir * self.distance_back
		render.line3d(self.node.pos.x, 0, self.node.pos.y, world_end_line.x, 0, world_end_line.y)

