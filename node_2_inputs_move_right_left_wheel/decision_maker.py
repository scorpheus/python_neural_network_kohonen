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


		if action & Actions.action_right_forward and action & Actions.action_left_backward:
			return True
		if action & Actions.action_right_backward and action & Actions.action_left_forward:
			return True

		if fragment.input_array[2] > random_set(0.5, 1.5) and fragment.input_array[0] < random_set(1, 3) and fragment.input_array[1] < 2 and (action & Actions.action_right_backward and action & Actions.action_left_backward):
			return True
		if fragment.input_array[2] > random_set(0.5, 1.5) and fragment.input_array[0] < random_set(1, 3) and fragment.input_array[1] > 2 and (action & Actions.action_left_forward):
			return True
		if fragment.input_array[2] > random_set(0.5, 1.5) and fragment.input_array[0] > random_set(1, 3) and fragment.input_array[1] < 2 and (action & Actions.action_right_forward):
			return True
		if fragment.input_array[2] <= random_set(0.5, 1.5) and action & Actions.action_right_forward and action & Actions.action_left_forward:
			return True

		# compute if it makes a big travel
		average = gs.Vector2(0, 0)
		for v in self.progress:
			average += v
		new_pos = self.node.actions.execute_action(action, self.node)
		average += new_pos
		average /= len(self.progress) + 1

		first_value = self.progress[0]
		self.progress.pop(0)
		self.progress.append(new_pos)

		if fragment.input_array[2] > 1 and fragment.input_array[0] > 2 and fragment.input_array[1] > 2:
			if gs.Vector2.Dist2(average, first_value) > (0.01 * 5)**2:
				return True

		return False
