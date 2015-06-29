__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions
import gs
from vector_helper import rotate


class Actions(BaseActions):

	action_left_forward_right_forward = 0
	action_left_backward_right_backward = 1
	action_left_forward_right_backward = 2
	action_left_backward_right_forward = 3

	def __init__(self):
		# compute nb of actions
		nb_actions = 4
		self.speed = 0.01

		super().__init__(nb_actions)
		self.action_names = ["left forward right forward", "left backward right backward", "left forward right backward", "left backward right forward"]

	def get_current_action_name(self, id_action):
		return self.action_names[id_action]

	def execute_action(self, action_type, node):
		new_pos = gs.Vector2(node.pos)
		if action_type == self.action_left_forward_right_forward:
			new_pos += node.dir * self.speed
		if action_type == self.action_left_backward_right_backward:
			new_pos -= node.dir * self.speed
		if action_type == self.action_left_forward_right_backward:
			rotate(node.dir, -self.speed*10)
		if action_type == self.action_left_backward_right_forward:
			rotate(node.dir, self.speed*10)
		return new_pos

