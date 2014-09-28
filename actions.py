__author__ = 'scorpheus'

# contain the actions the node can do


class BaseActions:

	def __init__(self, nb_actions):
		self.nb_actions = nb_actions

	def get_current_action_name(self, id_action):
		return ''

	def execute_action(self, action_type, node):
		pass