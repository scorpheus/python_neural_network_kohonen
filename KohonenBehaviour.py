__author__ = 'scorpheus'

from memory import Memory
from neural_network import NeuralNetwork
from Vec2D import Vec2d
import numpy as np


def range_adjust(k, a, b, u, v):
	return (k - a) / (b - a) * (v - u) + u


class KohonenBehaviour:
	def __init__(self, node_inputs, actions, decision_maker):

		self.node_inputs = node_inputs
		self.decision_maker = decision_maker

		self.memory = Memory(actions.nb_actions)

		self.neural_network = NeuralNetwork(self.node_inputs, actions.nb_actions, self.memory)

	def update(self):
		if False:    # training
			pass
		else:
			current_fragment = self.node_inputs.GetCurrentNodeFragment()

		# update the kohonen neural network with the new input
		#  get the action from the neural network for this fragment
		selected_action = self.neural_network.Update(current_fragment.input_array)

		# if the selected action is validate as good by the decision maker, keep in memory
		if self.decision_maker.is_good_action(current_fragment, selected_action):
			current_fragment.associated_action = selected_action
			self.memory.PushBackState(current_fragment)

		return selected_action

	def draw(self, pygame_draw, window):

		# draw neural network
		for input in range(self.neural_network.m_NbInput):
			y = (window.get_height()*0.5) / (self.neural_network.m_NbInput+1) * (input + 1)
			min = self.node_inputs.min_max_inputs[input][0]
			max = self.node_inputs.min_max_inputs[input][1]

			for id_neurone in range(self.neural_network.nb_neurone):
				value_input_neurone = self.neural_network.inputs_array[input][id_neurone]

				color = self.neural_network.neurone_action_array[id_neurone] / self.memory.nb_actions * 255
				pygame_draw.circle(window, (color, color, 255), Vec2d(int(range_adjust(value_input_neurone, min, max, 0, window.get_width())), int(y)), 1, 1)

		# draw memory
		if self.memory.fragment_array.shape[0] != 0:
			for fragment in range(self.memory.fragment_array.shape[0]):
				input_count = 0
				for value_input_neurone in np.nditer(self.memory.fragment_array[fragment].input_array):
					y = (window.get_height()*0.25) / (self.neural_network.m_NbInput+1) * (input_count + 1)
					min = self.node_inputs.min_max_inputs[input_count][0]
					max = self.node_inputs.min_max_inputs[input_count][1]

					color = self.memory.fragment_array[fragment].associated_action / self.memory.nb_actions * 255
					pygame_draw.circle(window, (color, color, 255), Vec2d(int(range_adjust(value_input_neurone, min, max, 0, window.get_width())), int(y)), 1, 1)

				input_count += 1



