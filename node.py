__author__ = 'scorpheus'

from KohonenBehaviour import KohonenBehaviour
import gs
import gs.plus.render as render
import gs.plus.input as plus_input
from render_helper import circle3d
from math import acos
from random import randrange


class Node:
	def __init__(self, actions, inputs, decision_maker):
		inputs.set_node(self)

		self.pos = gs.Vector2(0, 0)
		self.dir = gs.Vector2(1, 0)

		self.actions = actions
		self.inputs = inputs
		self.selected_action = 0

		self.timer_update = randrange(25)

		self.decision_maker = decision_maker
		decision_maker.set_node(self)

		self.kohonen_behaviour = KohonenBehaviour(self.inputs, self.actions, decision_maker)

		self.geo = render.load_geometry("@core/res/robot.geo")

		self.physic_world = None

	def update(self, physic_world):
		self.physic_world = physic_world

		self.inputs.update(physic_world)

		current_action = self.kohonen_behaviour.update()
		if self.timer_update <= 0:
			self.timer_update = randrange(25)
			self.selected_action = current_action
		self.timer_update -= 1

		new_pos = self.actions.execute_action(self.selected_action, self)
		#check no intersection with physic word
		if not physic_world.in_collision_with_spheres(new_pos, 1.0):
			self.pos = new_pos

		# move randomly somewhere
		if plus_input.key_down(gs.InputDevice.KeyR):
			while True:
				self.pos.x = -1 + randrange(100) * 0.01 * (10 - 1)
				self.pos.y = -1 + randrange(100) * 0.01 * (10 - 1)
				if not physic_world.in_collision_with_spheres(self.pos, 1):
					self.decision_maker.reset_progress(self.pos)
					break

	def draw(self):
		width = render.get_renderer().GetCurrentOutputWindow().GetSize().x
		height = render.get_renderer().GetCurrentOutputWindow().GetSize().y

		self.inputs.draw()

		angle_dir = acos(self.dir.Normalized().Dot(gs.Vector2(1, 0))) * (-1 if self.dir.y > 0 else 1)
		render.geometry3d(self.pos.x, 0, self.pos.y, self.geo, 0, angle_dir + 1.57, 0)
		circle3d(self.pos.x, self.pos.y, 0.5)

		half_width, half_height = width/2, height/2

		if self.pos.x > half_width:
			self.pos.x = half_width
		elif self.pos.x < -half_width:
			self.pos.x = -half_width
		elif self.pos.y > half_height:
			self.pos.y = half_height
		elif self.pos.y < -half_height:
			self.pos.y = -half_height
