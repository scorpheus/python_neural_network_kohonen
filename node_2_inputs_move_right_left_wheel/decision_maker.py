__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions
import gs
from random import randrange

def random_set(min, max):
	return min + randrange(100)* 0.01 * (max - min)


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

		self.progress = []
		self.reset_progress()

	def reset_progress(self):
		for i in range(10):
			self.progress.append(gs.Vector2(-1000, 0))


	def is_good_action(self, fragment, action):
		if action == 0:
			return False
		if action & Actions.action_left_backward and action & Actions.action_left_forward:
			return False
		if action & Actions.action_right_backward and action & Actions.action_right_forward:
			return False

		if fragment.input_array[0] > random_set(1, 2) and fragment.input_array[1] > random_set(1, 2) and action & Actions.action_right_forward and action & Actions.action_left_forward:
			return True

		if fragment.input_array[2] > random_set(0.75, 1.25) and fragment.input_array[0] < random_set(1, 2) and fragment.input_array[1] > random_set(1, 2) and action & Actions.action_right_forward and action & Actions.action_left_backward:
			return True
		if fragment.input_array[2] > random_set(0.75, 1.25) and fragment.input_array[0] > random_set(1, 2) and fragment.input_array[1] < random_set(1, 2) and action & Actions.action_right_backward and action & Actions.action_left_forward:
			return True

		if fragment.input_array[2] < random_set(0.75, 1.25) and fragment.input_array[0] < random_set(1, 2) and fragment.input_array[1] < random_set(1, 2) and \
			((action & Actions.action_right_backward and action & Actions.action_left_forward) or (action & Actions.action_right_forward and action & Actions.action_left_backward)):
			return True


		return False
