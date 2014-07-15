__author__ = 'scorpheus'

# contain the actions the node can do
from actions import BaseActions


class Actions(BaseActions):

	action_forward = 0
	action_turn_left = 1
	action_turn_right = 2

	def __init__(self):
		super().__init__(3)

	def execute_action(self, action_type, node):
		pass

