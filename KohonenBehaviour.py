__author__ = 'scorpheus'

from memory import Memory
from neural_network import NeuralNetwork
from Vec2D import Vec2d
import numpy as np
from random import randrange


def range_adjust(k, a, b, u, v):
	return (k - a) / (b - a) * (v - u) + u


class KohonenBehaviour:
	def __init__(self, node_inputs, actions, decision_maker):

		self.node_inputs = node_inputs
		self.decision_maker = decision_maker
		self.nb_actions = actions.nb_actions

		self.memory = Memory(actions.nb_actions)

		self.neural_network = NeuralNetwork(self.node_inputs, actions.nb_actions, self.memory)

	def update(self):
		map_neural_network_on_memory = True
		if False:    # training
			pass
		else:
			if randrange(100) < 3 and self.memory.GetNbFragment() > 0: # get a value from the memory to train de map, this is a test for the moment TODO
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

	def draw(self, pygame_draw, window):
		# return
		window_height = window.get_height()
		window_width = window.get_width()

		# draw neural network
		for input in range(self.neural_network.m_NbInput):
			y = (window_height*0.25) + (window_height*0.25) / (self.neural_network.m_NbInput+1) * (input + 1)
			val_input = self.node_inputs.min_max_inputs[input]
			min = val_input[0]
			max = val_input[1]

			for id_neurone in range(self.neural_network.nb_neurone):
				value_input_neurone = self.neural_network.inputs_array[input][id_neurone]

				color = 255
				if self.neural_network.neurone_action_array[id_neurone] != -1:
					color = self.neural_network.neurone_action_array[id_neurone] / self.memory.nb_actions * 255
				range_value_input = int(range_adjust(value_input_neurone, min, max, 0, window_width))
				pygame_draw.line(window, (color, color, 255), (range_value_input, int(y)), (range_value_input, int(y+20)))
		return
		# draw memory
		if self.memory.fragment_array.shape[0] != 0:
			for fragment in range(self.memory.fragment_array.shape[0]):
				input_count = 0
				for value_input_neurone in np.nditer(self.memory.fragment_array[fragment].input_array):
					y = (window_height*0.25) / (self.neural_network.m_NbInput+1) * (input_count + 1)
					min = self.node_inputs.min_max_inputs[input_count][0]
					max = self.node_inputs.min_max_inputs[input_count][1]

					color = self.memory.fragment_array[fragment].associated_action / self.memory.nb_actions * 255
					# pygame_draw.circle(window, (color, color, 255), Vec2d(int(range_adjust(value_input_neurone, min, max, 0, window.get_width())), int(y)), 1, 1)
					pygame_draw.line(window, (color, color, 255), (int(range_adjust(value_input_neurone, min, max, 0, window_width)), int(y)), (int(range_adjust(value_input_neurone, min, max, 0, window_width)), int(y+20)))

					input_count += 1



