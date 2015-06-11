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

	def __init__(self, nb_actions, nb_inputs):
		self.fragment_array = np.array([])

		self.fragments_inputs_array = np.empty((0, nb_inputs))
		self.fragments_associated_action_array = np.array([])

		# init the array for the count of nb fragment per action
		self.nb_actions = nb_actions
		self.m_NbFragmentPerActionArray = np.zeros(self.nb_actions)
		self.m_TabPercentFragmentPerAction = np.zeros(self.nb_actions)

	def load(self):
		self.fragment_array = np.load("fragment_array.npy")
		self.fragments_inputs_array = np.load("fragments_inputs_array.npy")
		self.fragments_associated_action_array = np.load("fragments_associated_action_array.npy")

	def save(self):
		np.save("fragment_array", self.fragment_array)
		np.save("fragments_inputs_array", self.fragments_inputs_array)
		np.save("fragments_associated_action_array", self.fragments_associated_action_array)


	def GetNbFragmentPerActionArray(self):
		return self.m_NbFragmentPerActionArray

	def GetNbFragment(self):
		return self.fragment_array.size

	def GetFragmentInputs(self, id_fragment):
		return self.fragments_inputs_array[id_fragment]

	def GetFragmentAssociatedAction(self, id_fragment):
		return self.fragments_associated_action_array[id_fragment]

	def FragmentAlreadyInside(self, fragment):
		return np.any(self.fragments_associated_action_array[np.where(np.equal(self.fragments_inputs_array, fragment.input_array).all(1))] == fragment.associated_action)
		# for id_frag in range(self.fragment_array.shape[0]):
		# 	frag = self.fragment_array[id_frag]
		# 	if np.array_equal(frag.input_array, fragment.input_array) and frag.associated_action == fragment.associated_action:
		# 		return True
		# return False

	def PushBackState(self, _NewFragment):
		if self.FragmentAlreadyInside(_NewFragment):
			return

		# increase the count of state per action
		self.m_NbFragmentPerActionArray[_NewFragment.associated_action] += 1

		# add the state into the pool
		self.fragment_array = np.append(self.fragment_array, [_NewFragment])

		self.fragments_inputs_array = np.vstack((self.fragments_inputs_array, _NewFragment.input_array))
		self.fragments_associated_action_array = np.append(self.fragments_associated_action_array, [_NewFragment.associated_action])

		# recheck the percent of fragment per actions
		self.ComputePercentPerAction()

	def ComputePercentPerAction(self):
		l_DivNbState = 1/self.GetNbFragment()

		self.m_TabPercentFragmentPerAction = self.m_NbFragmentPerActionArray * l_DivNbState * 100

