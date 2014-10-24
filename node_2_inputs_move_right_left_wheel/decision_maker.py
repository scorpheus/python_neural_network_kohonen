__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

	def is_good_action(self, fragment, action):
		if action == 0:
			return False
		if action & Actions.action_left_backward and action & Actions.action_left_forward:
			return False
		if action & Actions.action_right_backward and action & Actions.action_right_forward:
			return False

		if fragment.input_array[0] > 20 and fragment.input_array[1] > 20 and (action & Actions.action_right_forward or action & Actions.action_left_forward):
			return True
		if fragment.input_array[0] < 20 and fragment.input_array[1] < 20 and (action & Actions.action_right_backward or action & Actions.action_left_backward):
			return True
		if fragment.input_array[0] < 20 < fragment.input_array[1] and (action & Actions.action_right_backward or action & Actions.action_left_forward):
			return True
		if fragment.input_array[0] > 20 > fragment.input_array[1] and (action & Actions.action_right_forward or action & Actions.action_left_backward):
			return True


		if fragment.input_array[2] <= 10 and (action & Actions.action_right_forward and action & Actions.action_left_forward):
			return True

		return False
