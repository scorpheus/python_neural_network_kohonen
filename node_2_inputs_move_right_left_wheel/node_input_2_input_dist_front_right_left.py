__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import gs
from vector_helper import rotate


class NodeInputs(BaseNodeInputs):

	def __init__(self):
		super().__init__(3)

		# set the min max for the two input
		self.min_max_inputs[0][0] = 0
		self.min_max_inputs[0][1] = 10
		self.min_max_inputs[1][0] = 0
		self.min_max_inputs[1][1] = 10
		self.min_max_inputs[2][0] = 0
		self.min_max_inputs[2][1] = 5

		self.distance_left = 5
		self.distance_right = 5
		self.distance_back = 2

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(self.nb_inputs)

		# fill the fragment with the inputs from the node
		current_fragment.input_array[0] = self.distance_left
		current_fragment.input_array[1] = self.distance_right
		current_fragment.input_array[2] = self.distance_back

		return current_fragment

	def update(self, physic_world):
		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		self.distance_left = max(0, min(100, physic_world.intersection_line_spheres(self.node.pos, left_dir, 100)))

		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		self.distance_right = max(0, min(100, physic_world.intersection_line_spheres(self.node.pos, right_dir, 100)))

		# need value between 0 and 10
		self.distance_left = int(self.distance_left /10)
		self.distance_right = int(self.distance_right /10)

		back_dir = gs.Vector2(self.node.dir) * -1
		self.distance_back = max(0, min(50, physic_world.intersection_line_spheres(self.node.pos, back_dir, 50)))
		self.distance_back = int(self.distance_back /10)

	def draw(self, render, center):
		world_pos = self.node.pos + center

		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		world_end_line = self.node.pos + left_dir * self.distance_left * 10 + center
		render.line2d(world_pos.x, world_pos.y, world_end_line.x, world_end_line.y)

		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		world_end_line = self.node.pos + right_dir * self.distance_right * 10 + center
		render.line2d(world_pos.x, world_pos.y, world_end_line.x, world_end_line.y)

		back_dir = gs.Vector2(self.node.dir) * -1
		world_end_line = self.node.pos + back_dir * self.distance_back * 10 + center
		render.line2d(world_pos.x, world_pos.y, world_end_line.x, world_end_line.y)

