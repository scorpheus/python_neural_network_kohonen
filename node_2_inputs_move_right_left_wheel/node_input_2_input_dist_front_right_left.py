__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import gs
import gs.plus.render as render
from vector_helper import rotate


class NodeInputs(BaseNodeInputs):

	def __init__(self):
		super().__init__(3)

		# set the min max for the two input
		self.min_max_inputs[0][0] = 0
		self.min_max_inputs[0][1] = 4
		self.min_max_inputs[1][0] = 0
		self.min_max_inputs[1][1] = 4
		self.min_max_inputs[2][0] = 0
		self.min_max_inputs[2][1] = 2

		self.distance_left = 2.5
		self.distance_right = 2.5
		self.distance_back = 1

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(self.nb_inputs)

		# fill the fragment with the inputs from the node
		current_fragment.input_array[0] = self.distance_left
		current_fragment.input_array[1] = self.distance_right
		current_fragment.input_array[2] = self.distance_back

		return current_fragment

	def update(self, physic_world):
		side_dir = gs.Vector2(self.node.dir)
		rotate(side_dir, 90)
		side_dir /= 2

		# need 100 values not the intermediary, not necessary
		self.distance_left = int(self.distance_left * 10) / 10
		self.distance_right = int(self.distance_right * 10) / 10

		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		self.distance_left = max(0, min(4, physic_world.intersection_line_spheres(self.node.pos - side_dir, left_dir, 4)))

		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		self.distance_right = max(0, min(4, physic_world.intersection_line_spheres(self.node.pos + side_dir, right_dir, 4)))

		back_dir = gs.Vector2(self.node.dir) * -1
		self.distance_back = max(0, min(2, physic_world.intersection_line_spheres(self.node.pos, back_dir, 2)))

		# need 100 values not the intermediary, not necessary
		self.distance_left = int(self.distance_left * 10) / 10
		self.distance_right = int(self.distance_right * 10) / 10
		self.distance_back = int(self.distance_back * 10) / 10

	def draw(self):
		side_dir = gs.Vector2(self.node.dir)
		rotate(side_dir, 90)
		side_dir /= 2

		start_dir = self.node.pos - side_dir
		left_dir = gs.Vector2(self.node.dir)
		rotate(left_dir, -10.0)
		world_end_line = start_dir + left_dir * self.distance_left
		render.line3d(start_dir.x, 1.1, start_dir.y, world_end_line.x, 1.1, world_end_line.y)

		start_dir = self.node.pos + side_dir
		right_dir = gs.Vector2(self.node.dir)
		rotate(right_dir, 10.0)
		world_end_line = start_dir + right_dir * self.distance_right
		render.line3d(start_dir.x, 1.1, start_dir.y, world_end_line.x, 1.1, world_end_line.y)

		back_dir = gs.Vector2(self.node.dir) * -1
		world_end_line = self.node.pos + back_dir * self.distance_back
		render.line3d(self.node.pos.x, 1.1, self.node.pos.y, world_end_line.x, 1.1, world_end_line.y)
