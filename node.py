__author__ = 'scorpheus'

from KohonenBehaviour import KohonenBehaviour
import gs
from render_helper import circle2d
from gs.plus import *


class Node:
	def __init__(self, actions, inputs, decision_maker):
		inputs.set_node(self)

		self.pos = gs.Vector2(0, 0)
		self.dir = gs.Vector2(1, 0)

		self.actions = actions
		self.inputs = inputs
		self.selected_action = 0

		decision_maker.set_node(self)

		self.kohonen_behaviour = KohonenBehaviour(self.inputs, self.actions, decision_maker)

	def update(self, physic_world):
		self.inputs.update(physic_world)

		self.selected_action = self.kohonen_behaviour.update()

		new_pos = self.actions.execute_action(self.selected_action, self)
		#check no intersection with physic word
		if not physic_world.in_collision_with_spheres(new_pos, 5):
			self.pos = new_pos

	def draw(self):
		width = render.renderer.GetCurrentOutputWindow().GetSize().x
		height = render.renderer.GetCurrentOutputWindow().GetSize().y
		center = gs.Vector2(width/2, height/2)

		self.inputs.draw(center)
		self.kohonen_behaviour.draw(width, height)

		radius = 5
		pos = self.pos + center
		pos2 = self.pos + self.dir * radius + center

		circle2d(render, pos.x, pos.y, radius)
		render.line2d(pos.x, pos.y, pos2.x, pos2.y)

		half_width, half_height = width/2, height/2

		if self.pos.x > half_width:
			self.pos.x = half_width
		elif self.pos.x < -half_width:
			self.pos.x = -half_width
		elif self.pos.y > half_height:
			self.pos.y = half_height
		elif self.pos.y < -half_height:
			self.pos.y = -half_height
