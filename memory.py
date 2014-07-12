__author__ = 'scorpheus'

from action import nb_actions
import numpy as np

# the fragment contains only one event:
#   for a set of inputs, it have an action
#   all the fragments are saved in the memory

#   the current fragment is used to check the current inputs and action recorded when the kohonen behavior ask


class Fragment:

	def __init__(self, nb_input):
		self.input_array = np.zeros(nb_input)
		self.associated_action = 0


# the memory contains all the fragments


class Memory:

	def __init__(self):
		self.fragment_array = np.array([])

		# init the array for the count of nb fragment per action
		self.m_NbFragmentPerActionArray = np.zeros(nb_actions)

	def GetNbFragmentPerActionArray(self):
		return self.m_NbFragmentPerActionArray

	def GetFragmentArray(self):
		return self.fragment_array

	def GetNbFragment(self):
		return self.fragment_array.size

	def PushBackState(self, _NewState):
		# increase the count of state per action
		self.m_NbFragmentPerActionArray[_NewState.associated_action] += 1

		# add the state into the pool
		self.fragment_array.push_back(_NewState)
