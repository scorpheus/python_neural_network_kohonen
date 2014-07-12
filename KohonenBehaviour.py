__author__ = 'scorpheus'

from memory import Memory


class KohonenBehaviour:
	def __init__(self, node_inputs):
		self.node_inputs = node_inputs

		self.memory = Memory()
