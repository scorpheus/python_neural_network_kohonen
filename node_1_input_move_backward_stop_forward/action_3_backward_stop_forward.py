__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions
import copy


class Actions(BaseActions):

	action_backward = 0
	action_stop = 1
	action_forward = 2

	def __init__(self):
		super().__init__(3)
		self.action_names = ["backward", "stop", "forward"]

	def get_current_action_name(self, id_action):
		name = ""
		if id_action == self.action_backward:
			name += "backward"
		if id_action & self.action_stop:
			name += ", stop"
		if id_action & self.action_forward:
			name += ", backward"
		return name

	def execute_action(self, action_type, node):
		new_pos = copy.copy(node.pos)
		if action_type == self.action_backward:
			new_pos -= node.dir *1.0
		elif action_type == self.action_stop:
			pass
		elif action_type == self.action_forward:
			new_pos += node.dir *1.0

		return new_pos
