__author__ = 'scorpheus'

from node_inputs import NodeInputs
from memory import Fragment


class NodeInputs2InputsDetectorRightLeft(NodeInputs):

	def __init__(self):
		super().__init__()

	def GetCurrentNodeFragment(self, node):
		current_fragment = Fragment(0)

		# fill the fragment with the inputs from the node

		return current_fragment
