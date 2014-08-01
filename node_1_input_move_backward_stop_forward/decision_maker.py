__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_1_input_move_backward_stop_forward.action_3_backward_stop_forward import Actions


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

	def is_good_action(self, fragment, action):
		if fragment.input_array[0] < 20 and action == Actions.action_backward:
			return True
		elif fragment.input_array[0] == 21 and action == Actions.action_stop:
		 	return True
		elif fragment.input_array[0] > 21 and action == Actions.action_forward:
			return True
		return False
