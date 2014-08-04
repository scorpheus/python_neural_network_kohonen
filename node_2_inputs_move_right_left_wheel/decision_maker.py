__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

	action_left_backward = 0
	action_left_forward = 1
	action_right_backward = 2
	action_right_forward = 3

	def is_good_action(self, fragment, action):
		if fragment.input_array[0] > 20 and fragment.input_array[1] > 20 and (action == Actions.action_right_forward or action == Actions.action_left_forward):
			return True
		if fragment.input_array[0] < 20 and fragment.input_array[1] < 20 and (action == Actions.action_right_backward or action == Actions.action_left_backward):
			return True
		if fragment.input_array[0] < 20 < fragment.input_array[1] and (action == Actions.action_right_backward or action == Actions.action_left_forward):
			return True
		if fragment.input_array[0] > 20 > fragment.input_array[1] and (action == Actions.action_right_forward or action == Actions.action_left_backward):
			return True
		return False
