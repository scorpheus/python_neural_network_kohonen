__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action


class BaseDecisionMaker:

	def __init__(self):
		self.node = None

	def set_node(self, n):
		self.node = n

	def is_good_action(self, fragment, action):
		pass