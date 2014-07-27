__author__ = 'scorpheus'

import numpy as np
import math
import sys

class NeuralNetwork:
	nb_neurone = 50

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
		self.neurone_action_array = np.random.randint(nb_actions, size=self.nb_neurone)

		# array of m_NbInput for each input, containing each input range value
		self.inputs_array = [np.random.random_sample(self.nb_neurone) * (inputs.min_max_inputs[input][1]-inputs.min_max_inputs[input][0]) + inputs.min_max_inputs[input][0] for input in range(self.m_NbInput)]

		# contain max weight for each input
		self.m_MaxWeightInputsArray = np.ones(self.m_NbInput)
	
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
		l_ArrayNbFragmentsPerAction = np.zeros(self.m_MemoryGoodAction.nb_actions)
	
		for action in range(self.m_MemoryGoodAction.nb_actions):
			if l_MemoryNbFragmentPerAction[action] != 0:
				l_ArrayNbFragmentsPerAction[action] = 1.0/l_MemoryNbFragmentPerAction[action]

		l_UpdateTheMaxWeightArray = True
	
		# for all good state
		for id_fragment in range(l_nb_fragment):
			# find the input for each state
			l_current_fragment = l_fragment_array[id_fragment]
			
			# the action associate to this input
			l_GoodAction = l_current_fragment.associated_action
	
			#take the array of input from this state
			l_TempInputFragment = l_current_fragment.input_array
	
			# find the winner for this input
			l_id_neurone_winner = self.FindTheWinner(l_TempInputFragment, l_UpdateTheMaxWeightArray)

			# add this score to the neighbors
			for id_neurone in range(self.nb_neurone):

				l_SumDistance = 0

				# find the distance from the winner
				for input in range(self.m_NbInput):
					# For this neurone, the  sum of the input - the weight of this input with this neurone, it's an euclidean distance;
					l_WeightLinkValueWinner = self.inputs_array[input][l_id_neurone_winner] / self.m_MaxWeightInputsArray[input]
					l_WeightLinkValue = self.inputs_array[input][id_neurone] / self.m_MaxWeightInputsArray[input]
	
					l_SumDistance += (l_WeightLinkValueWinner - l_WeightLinkValue) * (l_WeightLinkValueWinner - l_WeightLinkValue)

				l_save_action_score_per_neuron[id_neurone][l_GoodAction] += math.exp((-(l_SumDistance)*l_DivActivationArea)*self.g_LearningRate) * l_ArrayNbFragmentsPerAction[l_GoodAction]
	
			# update the max weight array only once, just for the first loop
			l_UpdateTheMaxWeightArray = False

		# add to each neurone, the action associate to it
		for id_neurone in range(self.nb_neurone):
			l_MaxScore = 0
			l_SelectedAction = 0
	
			for action in range(self.m_MemoryGoodAction.nb_actions):
				if l_MaxScore < l_save_action_score_per_neuron[id_neurone][action]:
					l_SelectedAction = action
					l_MaxScore = l_save_action_score_per_neuron[id_neurone][action]

			# put to the node the associate action
			self.neurone_action_array[id_neurone] = l_SelectedAction

	def FindTheWinner(self, _InputArray, _UpdateTheMaxWeightArray):
		# for each neurone, compute the output from the input 
		# and find which one is the winner, with the less output value;

		if _UpdateTheMaxWeightArray:
			# put the max at the minimum
			self.m_MaxWeightInputsArray = np.ones(self.m_NbInput)
	
			# find the max weight for each neurone to after use it to make all the weight at the same level of power
			for id_neurone in range(self.nb_neurone):
				for input in range(self.m_NbInput):
					# For this neurone, check his weight to be the maximum
					l_WeightLinkValue = math.fabs(self.inputs_array[input][id_neurone])
	
					# check if it's the Max
					if l_WeightLinkValue > self.m_MaxWeightInputsArray[input]:
						self.m_MaxWeightInputsArray[input] = l_WeightLinkValue

			# check the max for the input
			for input in range(self.m_NbInput):
				# For this neurone, check his weight to be the maximum
				l_WeightLinkValue = math.fabs(_InputArray[input])

				# check if it's the Max
				if l_WeightLinkValue > self.m_MaxWeightInputsArray[input]:
					self.m_MaxWeightInputsArray[input] = l_WeightLinkValue

		# find the winner neurone
		l_MaxValue = sys.float_info.max
		l_CurrentWinner = 0

		for id_neurone in range(self.nb_neurone):
			l_Sum = 0

			for input in range(self.m_NbInput):

				# For this neurone, the  sum of the input - the weight of this input with this neurone, it's an euclidean distance;
				l_InputValue = _InputArray[input] / self.m_MaxWeightInputsArray[input]
				l_WeightLinkValue = self.inputs_array[input][id_neurone] / self.m_MaxWeightInputsArray[input]
	
				l_Sum += (l_InputValue - l_WeightLinkValue) * (l_InputValue - l_WeightLinkValue)

			# check if it's the winner
			if l_Sum <= l_MaxValue:
				l_MaxValue = l_Sum
				l_CurrentWinner = id_neurone
	
		return l_CurrentWinner

