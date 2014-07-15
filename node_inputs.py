__author__ = 'scorpheus'

from memory import Fragment
import numpy as np


class BaseNodeInputs:
	def __init__(self, nb_inputs):
		self.nb_inputs = nb_inputs
		self.min_max_inputs = np.empty((self.nb_inputs, 2))

	def set_node(self, node):
		self.node = node

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(0)

		# fill the fragment with the inputs from the node

		return current_fragment
