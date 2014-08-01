__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions


class Actions(BaseActions):

	action_backward = 0
	action_stop = 1
	action_forward = 2

	def __init__(self):
		super().__init__(3)

	def execute_action(self, action_type, node):
		if action_type == self.action_backward:
			node.pos -= node.dir *0.1
		elif action_type == self.action_stop:
			pass
		elif action_type == self.action_forward:
			node.pos += node.dir *0.1
