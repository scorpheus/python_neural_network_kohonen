__author__ = 'scorpheus'

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

	def __init__(self, nb_actions):
		self.fragment_array = np.array([])

		# init the array for the count of nb fragment per action
		self.nb_actions = nb_actions
		self.m_NbFragmentPerActionArray = np.zeros(self.nb_actions)
		self.m_TabPercentFragmentPerAction = np.zeros(self.nb_actions)

	def GetNbFragmentPerActionArray(self):
		return self.m_NbFragmentPerActionArray

	def GetNbFragment(self):
		return self.fragment_array.size

	def FragmentAlreadyInside(self, fragment):
		for id_frag in range(self.fragment_array.shape[0]):
			frag = self.fragment_array[id_frag]
			if np.array_equal(frag.input_array, fragment.input_array) and frag.associated_action == fragment.associated_action:
				return True
		return False

	def PushBackState(self, _NewFragment):
		if self.FragmentAlreadyInside(_NewFragment):
			return

		# increase the count of state per action
		self.m_NbFragmentPerActionArray[_NewFragment.associated_action] += 1

		# add the state into the pool
		self.fragment_array = np.append(self.fragment_array, [_NewFragment])

		# recheck the percent of fragment per actions
		self.ComputePercentPerAction()

	def ComputePercentPerAction(self):
		l_DivNbState = 1/self.GetNbFragment()

		for action in range(self.nb_actions):
			self.m_TabPercentFragmentPerAction[action] = self.m_NbFragmentPerActionArray[action] * l_DivNbState * 100

