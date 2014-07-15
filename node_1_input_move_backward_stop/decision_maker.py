__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_1_input_move_backward_stop.action_2_backward_stop import Actions


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

	def is_good_action(self, fragment, action):
		if fragment.input_array[0] < 20 and action == Actions.action_backward:
			return True
		elif fragment.input_array[0] > 30 and action == Actions.action_stop:
			return True
		return False
