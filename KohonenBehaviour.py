__author__ = 'scorpheus'

from memory import Memory
from neural_network import NeuralNetwork
import numpy as np
from random import randrange
import gs
import gs.plus.input as plus_input
import gs.plus.render as render


def range_adjust(k, a, b, u, v):
	return (k - a) / (b - a) * (v - u) + u


memory = None
neural_network = None

class KohonenBehaviour:
	def __init__(self, node_inputs, actions, decision_maker):
		global memory
		global neural_network

		self.node_inputs = node_inputs
		self.decision_maker = decision_maker
		self.nb_actions = actions.nb_actions

		if memory is None:
			memory = Memory(actions.nb_actions, node_inputs.nb_inputs)

		if neural_network is None:
			neural_network = NeuralNetwork(self.node_inputs, actions.nb_actions, memory)

		self.last_messed_up_nb_fragment_in_memory = 0

		self.color_array = [gs.Color.White, gs.Color.Grey, gs.Color.Red, gs.Color.Green, gs.Color.Blue, gs.Color.Yellow, gs.Color.Orange, gs.Color.Purple,
							gs.Color(0.5, 0, 0), gs.Color(0, 0.5, 0), gs.Color(0, 0, 0.5), gs.Color(0.5, 0.5, 0), gs.Color(0, 0.5, 0.5), gs.Color(0.5, 0, 0.5), gs.Color(0.5, 1, 0), gs.Color(1, 0.5, 0), ]

	def update(self):

		if plus_input.key_down(gs.InputDevice.KeyA):
			memory.save()

		if plus_input.key_down(gs.InputDevice.KeyZ):
			memory.load()

		if plus_input.key_down(gs.InputDevice.KeyM) or memory.GetNbFragment() - self.last_messed_up_nb_fragment_in_memory > 1500:
			self.last_messed_up_nb_fragment_in_memory = memory.GetNbFragment()
			neural_network.MessedUpNeuroneInputs(self.node_inputs)

		not_training_use_directly_the_brain = False
		if not_training_use_directly_the_brain:
			current_fragment = self.node_inputs.GetCurrentNodeFragment()
			map_neural_network_on_memory = False
		else:
			map_neural_network_on_memory = True
			if randrange(100) < 30 and memory.GetNbFragment() > 0: # get a value from the memory to train de map, this is a test for the moment TODO
				# print('random fragment: '+str(randrange(memory.GetNbFragment())))
				current_fragment = memory.fragment_array[randrange(memory.GetNbFragment())]
			else:
				current_fragment = self.node_inputs.GetCurrentNodeFragment()
				map_neural_network_on_memory = False

		# randomly label the neurone to keep it fresh with the new input
		if randrange(1000) == 1 and memory.GetNbFragment() > 0:
			neural_network.labelling()

		# update the kohonen neural network with the new input
		#  get the action from the neural network for this fragment
		selected_action = int(neural_network.Update(current_fragment.input_array, map_neural_network_on_memory))

		if not not_training_use_directly_the_brain:
		# sometime don't listen to the brain and do instinct stupidity
			if randrange(1000) < 30 or selected_action == -1:
				selected_action = randrange(self.nb_actions)

		# if the selected action is validate as good by the decision maker, keep in memory
		if self.decision_maker.is_good_action(current_fragment, selected_action):
			# add the framgent only it there not too much of this one already in memory
			if memory.m_TabPercentFragmentPerAction[selected_action] < 1/self.nb_actions*100 + 30:
				current_fragment.associated_action = selected_action
				memory.PushBackState(current_fragment)

		return selected_action

	def draw(self, width, height):
		if not plus_input.key_down(gs.InputDevice.KeyK):
			return

		width = width-10

		# draw neural network
		previous_point = np.empty((neural_network.nb_neurone))
		y_part = (height*0.75) / (neural_network.m_NbInput+1)
		color = gs.Color(1, 1, 1)
		for input in range(neural_network.m_NbInput):
			y = (height*0.25) + y_part * (input + 1)
			val_input = self.node_inputs.min_max_inputs[input]
			min = val_input[0]
			max = val_input[1]

			for id_neurone in range(neural_network.nb_neurone):
				value_input_neurone = neural_network.inputs_array[input][id_neurone]

				if neural_network.neurone_action_array[id_neurone] != -1:
					color = self.color_array[neural_network.neurone_action_array[id_neurone]]
				range_value_input = range_adjust(value_input_neurone, min, max, 10, width)
				render.line2d(range_value_input, y, range_value_input, y+2, color, color)

				if input != 0:
					render.line2d(previous_point[id_neurone], y-y_part+2, range_value_input, y, color, color)
				previous_point[id_neurone] = range_value_input

		# return

		# draw memory
		if memory.fragment_array.shape[0] != 0:
			for fragment in range(memory.fragment_array.shape[0]):
				input_count = 0
				color = self.color_array[memory.fragment_array[fragment].associated_action]

				for value_input_neurone in np.nditer(memory.fragment_array[fragment].input_array):
					y = (height*0.25) / (neural_network.m_NbInput+1) * (input_count + 1)
					val_input = self.node_inputs.min_max_inputs[input_count]
					min = val_input[0]
					max = val_input[1]

					range_value_int = range_adjust(value_input_neurone, min, max, 10, width) + randrange(100)*0.1
					render.line2d(range_value_int, y, range_value_int, y+20, color, color)

					input_count += 1



