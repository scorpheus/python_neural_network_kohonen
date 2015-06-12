__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions
import gs


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()

		self.progress = []
		for i in range(10):
			self.progress.append(gs.Vector2(-1000, 0))

	def is_good_action(self, fragment, action):
		average = gs.Vector2(0, 0)
		for v in self.progress:
			average += v
		new_pos = self.node.actions.execute_action(action, self.node)
		average += new_pos
		average /= len(self.progress) + 1

		if gs.Vector2.Dist2(average, self.progress[0]) > (0.1 * 5)**2:
			self.progress.pop(0)
			self.progress.append(new_pos)
			return True

		return False
