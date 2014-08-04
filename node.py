__author__ = 'scorpheus'

from Vec2D import Vec2d
from KohonenBehaviour import KohonenBehaviour


class Node:
	def __init__(self, actions, inputs, decision_maker):
		inputs.set_node(self)

		self.pos = Vec2d(0, 0)
		self.dir = Vec2d(1, 0)

		self.actions = actions
		self.inputs = inputs
		self.selected_action = 0

		self.kohonen_behaviour = KohonenBehaviour(self.inputs, self.actions, decision_maker)

	def update(self, physic_world):
		self.inputs.update(physic_world)

		self.selected_action = self.kohonen_behaviour.update()

		self.actions.execute_action(self.selected_action, self)

	def draw(self, pygame_draw, window):
		self.inputs.draw(pygame_draw, window)
		self.kohonen_behaviour.draw(pygame_draw, window)

		radius = 5
		integer_pos = Vec2d(int(self.pos.x), int(self.pos.y))
		pygame_draw.circle(window, (255, 255, 255), integer_pos + window.get_rect().center, radius, 1)
		pygame_draw.line(window, (255, 255, 255), integer_pos + window.get_rect().center, integer_pos + self.dir*radius + window.get_rect().center)

		if integer_pos.x > window.get_rect().width*0.5:
			self.pos.x = window.get_rect().width*0.5
		elif integer_pos.x < -window.get_rect().width*0.5:
			self.pos.x = -window.get_rect().width*0.5
		elif integer_pos.y > window.get_rect().height*0.5:
			self.pos.y = window.get_rect().height*0.5
		elif integer_pos.y < -window.get_rect().height*0.5:
			self.pos.y = -window.get_rect().height*0.5
