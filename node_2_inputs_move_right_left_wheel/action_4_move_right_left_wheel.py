__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions


class Actions(BaseActions):

	action_left_backward = 0
	action_left_forward = 1
	action_right_backward = 2
	action_right_forward = 3

	def __init__(self):
		super().__init__(4)

	def execute_action(self, action_type, node):
		if action_type == self.action_left_backward:
			node.dir.rotate(0.1)
			node.pos -= node.dir *0.1
		elif action_type == self.action_left_forward:
			node.dir.rotate(0.1)
			node.pos += node.dir *0.1
		elif action_type == self.action_right_backward:
			node.dir.rotate(-0.1)
			node.pos -= node.dir *0.1
		elif action_type == self.action_right_forward:
			node.dir.rotate(-0.1)
			node.pos += node.dir *0.1

