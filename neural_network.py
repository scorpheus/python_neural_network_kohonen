__author__ = 'scorpheus'

import numpy as np
import math
import sys

class NeuralNetwork:
	nb_neurone = 200

	START_ACTIVATION_AREA = 0.20
	START_LEARNING_RATE = 0.30
	
	def __init__(self, inputs, nb_actions, _MemoryGoodAction):

		self.g_ActivationArea = self.START_ACTIVATION_AREA
		self.g_LearningRate = self.START_LEARNING_RATE
		self.m_InLearning = False
	
		# save the state Memory of good action
		self.m_MemoryGoodAction = _MemoryGoodAction

		self.m_NbInput = inputs.nb_inputs

		# create the neuronal arrays
		# for the action labelled per neurone
		self.neurone_action_array = np.empty(self.nb_neurone)
		self.neurone_action_array.fill(-1)

		# array of m_NbInput for each input, containing each input range value
		self.inputs_array = np.array([np.random.random_sample(self.nb_neurone) * (inputs.min_max_inputs[input][1]-inputs.min_max_inputs[input][0]) + inputs.min_max_inputs[input][0] for input in range(self.m_NbInput)])

		# contain max weight for each input
		self.m_MaxWeightInputsArray = np.ones(self.m_NbInput)

	def MessedUpNeuroneInputs(self, inputs):
		# each input are rearrange in random position per neurone
		self.inputs_array = np.array([np.random.random_sample(self.nb_neurone) * (inputs.min_max_inputs[input][1]-inputs.min_max_inputs[input][0]) + inputs.min_max_inputs[input][0] for input in range(self.m_NbInput)])

		self.g_ActivationArea = self.START_ACTIVATION_AREA
		self.g_LearningRate = self.START_LEARNING_RATE

	def Update(self, _InputArray, _map_neural_network_to_memory):
	
		self.g_ActivationArea -= 0.0005
		#
		# if(g_System->GetKeyboardManager().GetKeyState('U') && !g_System->GetKeyboardManager().GetKeyLastState('U'))
		# {
		# 	g_ActivationArea -= 0.4f;
		# }
		# if(g_System->GetKeyboardManager().GetKeyState('I') && !g_System->GetKeyboardManager().GetKeyLastState('I'))
		# {
		# 	g_ActivationArea += 0.4f;
		# }
	
		if self.g_ActivationArea < 0.01:
			self.g_ActivationArea = 0.01
		
		self.g_LearningRate -= 0.0005
	
		if self.g_LearningRate < 0.01:
			self.g_LearningRate = 0.01
	
			# the network just finish to learn, so label to be sure
			if self.m_InLearning:
				self.m_InLearning = False
				self.labelling()

		#
		# g_System->GetTextManager().DrawText(V2Di(10,70), false, NULL, "Activation area: %.3f",  g_ActivationArea);
		# g_System->GetTextManager().DrawText(V2Di(10,90), false, NULL, "Learning Rate: %.4f", g_LearningRate);
		#
		#
		# for each neurone, compute the output from the input 
		# and find which one is the winner, with the less output value;
		
		# create the float array
		l_CurrentWinner = self.FindTheWinner(_InputArray, True)

		if _map_neural_network_to_memory:
			# save this division for the activation area
			l_DivActivationArea = 1/(2 * self.g_ActivationArea*self.g_ActivationArea)

			# knowing who is the winner, update his weight and the weight of his neighbors
			for id_neurone in range(self.nb_neurone):

				l_SumDistance = 0

				# find the distance from the winner
				for input in range(self.m_NbInput):

					# For this neurone, the  sum of the input - the weight of this input with this neurone, it's an euclidean distance;
					l_WeightLinkValueWinner = self.inputs_array[input][l_CurrentWinner] / self.m_MaxWeightInputsArray[input]
					l_WeightLinkValue = self.inputs_array[input][id_neurone] / self.m_MaxWeightInputsArray[input]

					l_SumDistance += (l_WeightLinkValueWinner - l_WeightLinkValue) * (l_WeightLinkValueWinner - l_WeightLinkValue)


				l_Distance = math.exp((-(l_SumDistance*l_DivActivationArea))) * self.g_LearningRate

				for input in range(self.m_NbInput):

					# For this neurone, the  sum of the input - the weight of this input with this neurone, it's an euclidean distance;
					l_InputValue = _InputArray[input]
					l_WeightLinkValue = self.inputs_array[input][id_neurone]

					self.inputs_array[input][id_neurone] = l_WeightLinkValue + l_Distance*(l_InputValue - l_WeightLinkValue)

			## for the winner, update and put his own input entry to the near state
			#for(jint i= 0; i<m_NbInput; ++i)
			#{
			#	# For this neurone, the  sum of the input - the weight of this input with this neurone, it's an euclidean distance;
			#	l_InputValue = _InputArray[i];
			#	l_WeightLinkValue = m_NeuronalArray[1]->at(l_CurrentWinner)->m_TabInput[i];

			#	m_NeuronalArray[1]->at(l_CurrentWinner)->m_TabInput[i] = l_WeightLinkValue + (l_InputValue - l_WeightLinkValue);
			#}

		return self.neurone_action_array[l_CurrentWinner]

	def labelling(self):
		#  find which action match to the node
		# from the memory to the neural network
	
		if not self.m_MemoryGoodAction:
			return True #if this doesn't exist , don't lose time to labelling

		# save the score for each action on each neurone and fill with 0
		l_save_action_score_per_neuron = np.zeros((self.nb_neurone, self.m_MemoryGoodAction.nb_actions))

		#take from the state Memory who already have a good action
		l_fragment_array = self.m_MemoryGoodAction.fragment_array
		l_nb_fragment = self.m_MemoryGoodAction.GetNbFragment()
	
		# save this division for the activation area
		l_DivActivationArea = 1.0 / (2.0 * self.g_ActivationArea * self.g_ActivationArea)
	
		# array for the number of each action, because if one action have 100 inputs and another one just 2 inputs, it's unfair and the count is false
		l_MemoryNbFragmentPerAction = self.m_MemoryGoodAction.GetNbFragmentPerActionArray()

		l_ArrayNbFragmentsPerAction = 1.0/l_MemoryNbFragmentPerAction
		l_ArrayNbFragmentsPerAction[l_ArrayNbFragmentsPerAction == np.inf] = 0

		l_UpdateTheMaxWeightArray = True


		# # find the winner for this input
		l_id_neurone_winner = self.FindTheWinner(self.m_MemoryGoodAction.fragments_inputs_array, l_UpdateTheMaxWeightArray)

		# add this score to the neighbors
		# weight link for the winner for each fragment
		l_WeightLinkValueWinner = np.swapaxes(self.inputs_array[:, l_id_neurone_winner], 0, 1) / self.m_MaxWeightInputsArray[:, :]
		l_WeightLinkValue = self.inputs_array[np.newaxis, :, :] / self.m_MaxWeightInputsArray[:, :, np.newaxis]

		l_SumDistance = ((l_WeightLinkValueWinner[:, :, np.newaxis] - l_WeightLinkValue)**2).sum(axis=1)

		# for each neurons and for this particular good action, add the score by the formula
		count = 0
		for associated_action in self.m_MemoryGoodAction.fragments_associated_action_array:
			# for each neurons and for this particular good action, add the score by the formula
			l_save_action_score_per_neuron[:, associated_action] += np.exp((-(l_SumDistance[count])*l_DivActivationArea)*self.g_LearningRate) * l_ArrayNbFragmentsPerAction[associated_action]
			count += 1

		# update the max weight array only once, just for the first loop
		l_UpdateTheMaxWeightArray = False


		# for all good state
		# for l_current_fragment in l_fragment_array:
		#
		# 	# the action associate to this input
		# 	l_GoodAction = l_current_fragment.associated_action
		#
		# 	#take the array of input from this state
		# 	l_TempInputFragment = l_current_fragment.input_array
		#
		# 	# find the winner for this input
		# 	l_id_neurone_winner = self.FindTheWinner(l_TempInputFragment, l_UpdateTheMaxWeightArray)
		#
		# 	# add this score to the neighbors
		# 	l_WeightLinkValueWinner = self.inputs_array[:, l_id_neurone_winner] / self.m_MaxWeightInputsArray
		# 	l_WeightLinkValue = self.inputs_array / self.m_MaxWeightInputsArray[:,  np.newaxis]
		#
		# 	l_SumDistance = ((l_WeightLinkValueWinner[:, np.newaxis] - l_WeightLinkValue)**2).sum(axis=0)
		#
		# 	# for each neurons and for this particular good action, add the score by the formula
		# 	l_save_action_score_per_neuron[:, l_GoodAction] += np.exp((-(l_SumDistance)*l_DivActivationArea)*self.g_LearningRate) * l_ArrayNbFragmentsPerAction[l_GoodAction]
		#
		# 	# update the max weight array only once, just for the first loop
		# 	l_UpdateTheMaxWeightArray = False

		# add to each neurone, the action associate to it
		# put to the node the associate action
		self.neurone_action_array = np.argmax(l_save_action_score_per_neuron, axis=1)

	def FindTheWinner(self, _InputArray, _UpdateTheMaxWeightArray):
		# for each neurone, compute the output from the input 
		# and find which one is the winner, with the less output value;

		if _UpdateTheMaxWeightArray:
			# find the max weight for each neurone to use it to make all the weight at the same level of power
			#find the max in the inputs array and max from the _InputArray
			self.m_MaxWeightInputsArray = np.maximum(np.amax(np.absolute(self.inputs_array), axis=1), np.absolute(_InputArray))

		# find the winner neurone
		l_InputValue = _InputArray / self.m_MaxWeightInputsArray
		if len(_InputArray.shape) > 1:
			l_WeightLinkValue = self.inputs_array[np.newaxis, :] / self.m_MaxWeightInputsArray[:, :, np.newaxis]
			l_CurrentWinner = ((l_InputValue[:,:, np.newaxis] - l_WeightLinkValue)**2).sum(axis=1).argmin(axis=1)
		else:
			l_WeightLinkValue = self.inputs_array / self.m_MaxWeightInputsArray[:,  np.newaxis]
			l_CurrentWinner = ((l_InputValue[:, np.newaxis] - l_WeightLinkValue)**2).sum(axis=0).argmin()

		return l_CurrentWinner

