__author__ = 'scorpheus'

# for a particular fragment, check if it's a good action
from decision_maker import BaseDecisionMaker
import gs


class DecisionMaker(BaseDecisionMaker):

	def __init__(self):
		super().__init__()
		self.progress = []
		self.reset_progress(gs.Vector2(0, 0))

	def reset_progress(self, pos):
		for i in range(10):
			self.progress.append(pos)

	def is_good_action(self, fragment, action):
		# if not self.node.physic_world.in_collision_with_spheres(self.node.pos, 1.0):
		# 	return True

		# if the bot make some progress and don't bump on the sphere
		average = gs.Vector2(0, 0)
		for v in self.progress:
			average += v
		new_pos = self.node.actions.execute_action(action, self.node)
		average += new_pos
		average /= len(self.progress) + 1

		if gs.Vector2.Dist2(average, self.progress[0]) > (0.01 * 5)**2 and \
				not self.node.physic_world.in_collision_with_spheres(self.node.pos, 1.0):
			self.progress.pop(0)
			self.progress.append(new_pos)
			return True

		return False
