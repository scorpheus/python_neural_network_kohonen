__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment
import gs
from gs.plus import key_down

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

	def update(self, physic_world):
		if key_down(gs.InputDevice.KeyR):
			self.distance_front = 0 if self.distance_front - 0.1 < 0 else self.distance_front - 0.1
		elif key_down(gs.InputDevice.KeyT):
			self.distance_front = 100 if self.distance_front + 0.1 > 100 else self.distance_front + 0.1

		front_dir = gs.Vector2(self.node.dir)

		self.distance_front = max(0, min(100, physic_world.intersection_line_spheres(self.node.pos, front_dir, 100)))

	def draw(self, render, center):
		world_pos = self.node.pos + center

		world_end_line = self.node.pos + self.node.dir * self.distance_front + center
		render.line2d(world_pos.x, world_pos.y, world_end_line.x, world_end_line.y)
