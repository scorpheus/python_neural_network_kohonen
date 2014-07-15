__author__ = 'scorpheus'

from node_inputs import BaseNodeInputs
from memory import Fragment


class NodeInputs2InputsDetectorRightLeft(BaseNodeInputs):

	def __init__(self):
		super().__init__(2)

	def GetCurrentNodeFragment(self):
		current_fragment = Fragment(0)

		# fill the fragment with the inputs from the node

		return current_fragment
