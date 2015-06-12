__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions
import gs
from vector_helper import rotate


class Actions(BaseActions):

	action_left_backward = 1
	action_left_forward = 2
	action_right_backward = 4
	action_right_forward = 8

	def __init__(self):
		# compute nb of actions
		nb_actions = 4 * 4
		self.speed = 0.01
		self.rot_speed = 0.1

		super().__init__(nb_actions)
		self.action_names = ["left backward", "left forward", "right backward", "right forward"]

	def get_current_action_name(self, id_action):
		name = ""

		if id_action & self.action_left_backward:
			name += "left backward"
		if id_action & self.action_left_forward:
			name += ", left forward"
		if id_action & self.action_right_backward:
			name += ", right backward"
		if id_action & self.action_right_forward:
			name += ", right forward"
		return name

	def execute_action(self, action_type, node):
		new_pos = gs.Vector2(node.pos)
		if action_type & self.action_left_backward:
			rotate(node.dir, self.rot_speed)
			new_pos -= node.dir * self.speed
		if action_type & self.action_left_forward:
			rotate(node.dir, -self.rot_speed)
			new_pos += node.dir * self.speed
		if action_type & self.action_right_backward:
			rotate(node.dir, -self.rot_speed)
			new_pos -= node.dir * self.speed
		if action_type & self.action_right_forward:
			rotate(node.dir, self.rot_speed)
			new_pos += node.dir * self.speed
		return new_pos

