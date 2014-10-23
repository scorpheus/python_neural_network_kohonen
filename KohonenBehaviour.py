__author__ = 'scorpheus'

import pygame
from memory import Memory
from neural_network import NeuralNetwork
import numpy as np
from random import randrange


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

	def update(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_m] or self.memory.GetNbFragment() - self.last_messed_up_nb_fragment_in_memory > 200:
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

	def draw(self, pygame_draw, window):
		pressed = pygame.key.get_pressed()
		if not pressed[pygame.K_k]:
			return

		window_height = window.get_height()
		window_width = window.get_width()-10

		# draw neural network
		previous_point = np.empty((self.neural_network.nb_neurone))
		y_part = (window_height*0.25) / (self.neural_network.m_NbInput+1)
		for input in range(self.neural_network.m_NbInput):
			y = (window_height*0.25) + y_part * (input + 1)
			val_input = self.node_inputs.min_max_inputs[input]
			min = val_input[0]
			max = val_input[1]

			for id_neurone in range(self.neural_network.nb_neurone):
				value_input_neurone = self.neural_network.inputs_array[input][id_neurone]

				color = 255
				if self.neural_network.neurone_action_array[id_neurone] != -1:
					color = self.neural_network.neurone_action_array[id_neurone] / self.memory.nb_actions * 255
				range_value_input = int(range_adjust(value_input_neurone, min, max, 10, window_width))
				pygame_draw.line(window, (color, color, 255), (range_value_input, int(y)), (range_value_input, int(y+20)))

				if input != 0:
					pygame_draw.line(window, (color, color, 255), (previous_point[id_neurone], int(y-y_part+20)), (range_value_input, int(y)))
				previous_point[id_neurone] = range_value_input

		# return

		# draw memory
		if self.memory.fragment_array.shape[0] != 0:
			for fragment in range(self.memory.fragment_array.shape[0]):
				input_count = 0
				color = self.memory.fragment_array[fragment].associated_action / self.memory.nb_actions * 255

				for value_input_neurone in np.nditer(self.memory.fragment_array[fragment].input_array):
					y = (window_height*0.25) / (self.neural_network.m_NbInput+1) * (input_count + 1)
					val_input = self.node_inputs.min_max_inputs[input_count]
					min = val_input[0]
					max = val_input[1]

					range_value_int = int(range_adjust(value_input_neurone, min, max, 10, window_width))
					pygame_draw.line(window, (color, color, 255), (range_value_int, int(y)), (range_value_int, int(y+20)))

					input_count += 1



