__author__ = 'scorpheus'

from memory import Memory
from neural_network import NeuralNetwork
import numpy as np
from random import randrange
import gs
from gs.plus import *


def range_adjust(k, a, b, u, v):
	return (k - a) / (b - a) * (v - u) + u


class KohonenBehaviour:
	def __init__(self, node_inputs, actions, decision_maker):

		self.node_inputs = node_inputs
		self.decision_maker = decision_maker
		self.nb_actions = actions.nb_actions

		self.memory = Memory(actions.nb_actions, node_inputs.nb_inputs)

		self.neural_network = NeuralNetwork(self.node_inputs, actions.nb_actions, self.memory)

		self.last_messed_up_nb_fragment_in_memory = 0

		self.color_array = [gs.Color.White, gs.Color.Grey, gs.Color.Red, gs.Color.Green, gs.Color.Blue, gs.Color.Yellow, gs.Color.Orange, gs.Color.Purple,
							gs.Color(0.5, 0, 0), gs.Color(0, 0.5, 0), gs.Color(0, 0, 0.5), gs.Color(0.5, 0.5, 0), gs.Color(0, 0.5, 0.5), gs.Color(0.5, 0, 0.5), gs.Color(0.5, 1, 0), gs.Color(1, 0.5, 0), ]

	def update(self):

		if key_down(gs.InputDevice.KeyA):
			self.memory.save()

		if key_down(gs.InputDevice.KeyZ):
			self.memory.load()

		if key_down(gs.InputDevice.KeyM) or self.memory.GetNbFragment() - self.last_messed_up_nb_fragment_in_memory > 1500:
			self.last_messed_up_nb_fragment_in_memory = self.memory.GetNbFragment()
			self.neural_network.MessedUpNeuroneInputs(self.node_inputs)

		map_neural_network_on_memory = True
		if False:    # training
			pass
		else:
			if randrange(100) < 30 and self.memory.GetNbFragment() > 0: # get a value from the memory to train de map, this is a test for the moment TODO
				# print('random fragment: '+str(randrange(self.memory.GetNbFragment())))
				current_fragment = self.memory.fragment_array[randrange(self.memory.GetNbFragment())]
			else:
				current_fragment = self.node_inputs.GetCurrentNodeFragment()
				map_neural_network_on_memory = False

		# randomly label the neurone to keep it fresh with the new input
		if randrange(1000) == 1 and self.memory.GetNbFragment() > 0:
			self.neural_network.labelling()

		# update the kohonen neural network with the new input
		#  get the action from the neural network for this fragment
		selected_action = int(self.neural_network.Update(current_fragment.input_array, map_neural_network_on_memory))

		# sometime don't listen to the brain and do instinct stupidity
		if randrange(1000) < 30 or selected_action == -1:
			selected_action = randrange(self.nb_actions)

		# if the selected action is validate as good by the decision maker, keep in memory
		if self.decision_maker.is_good_action(current_fragment, selected_action):
			# add the framgent only it there not too much of this one already in memory
			if self.memory.m_TabPercentFragmentPerAction[selected_action] < 1/self.nb_actions*100 + 30:
				current_fragment.associated_action = selected_action
				self.memory.PushBackState(current_fragment)

		return selected_action

	def draw(self, width, height):
		if not key_down(gs.InputDevice.KeyK):
			return

		width = width-10

		# draw neural network
		previous_point = np.empty((self.neural_network.nb_neurone))
		y_part = (height*0.25) / (self.neural_network.m_NbInput+1)
		color = gs.Color(1, 1, 1)
		for input in range(self.neural_network.m_NbInput):
			y = (height*0.25) + y_part * (input + 1)
			val_input = self.node_inputs.min_max_inputs[input]
			min = val_input[0]
			max = val_input[1]

			for id_neurone in range(self.neural_network.nb_neurone):
				value_input_neurone = self.neural_network.inputs_array[input][id_neurone]

				if self.neural_network.neurone_action_array[id_neurone] != -1:
					color = self.color_array[self.neural_network.neurone_action_array[id_neurone]]
				range_value_input = range_adjust(value_input_neurone, min, max, 10, width)
				render.line2d(range_value_input, y, range_value_input, y+20, color, color)

				if input != 0:
					render.line2d(previous_point[id_neurone], y-y_part+20, range_value_input, y, color, color)
				previous_point[id_neurone] = range_value_input

		# return

		# draw memory
		if self.memory.fragment_array.shape[0] != 0:
			for fragment in range(self.memory.fragment_array.shape[0]):
				input_count = 0
				color = self.color_array[self.memory.fragment_array[fragment].associated_action]

				for value_input_neurone in np.nditer(self.memory.fragment_array[fragment].input_array):
					y = (height*0.25) / (self.neural_network.m_NbInput+1) * (input_count + 1)
					val_input = self.node_inputs.min_max_inputs[input_count]
					min = val_input[0]
					max = val_input[1]

					range_value_int = range_adjust(value_input_neurone, min, max, 10, width)
					render.line2d(range_value_int, y, range_value_int, y+20, color, color)

					input_count += 1



