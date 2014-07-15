__author__ = 'scorpheus'

from memory import Memory
from neural_network import NeuralNetwork


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