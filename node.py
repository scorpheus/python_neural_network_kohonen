__author__ = 'scorpheus'

from simple_vec2d import SimpleVec2D
from KohonenBehaviour import KohonenBehaviour


class Node:
	def __init__(self, actions, inputs, decision_maker):
		inputs.set_node(self)

		self.pos = SimpleVec2D(0, 0)
		self.dir = SimpleVec2D(1, 0)

		self.actions = actions
		self.inputs = inputs
		self.selected_action = 0

		self.kohonen_behaviour = KohonenBehaviour(self.inputs, self.actions, decision_maker)

	def update(self, physic_world):
		self.inputs.update(physic_world)

		self.selected_action = self.kohonen_behaviour.update()

		new_pos = self.actions.execute_action(self.selected_action, self)
		#check no intersection with physic word
		if not physic_world.in_collision_with_spheres(new_pos, 5):
			self.pos = new_pos

	def draw(self, pygame_draw, window):
		self.inputs.draw(pygame_draw, window)
		self.kohonen_behaviour.draw(pygame_draw, window)

		radius = 5
		integer_pos = SimpleVec2D(int(self.pos.x), int(self.pos.y))
		pos = integer_pos + window.get_rect().center
		pos2 = integer_pos + self.dir*radius + window.get_rect().center
		pygame_draw.circle(window, (255, 255, 255), pos, radius, 1)
		pygame_draw.line(window, (255, 255, 255), pos, pos2)

		if self.pos.x > window.get_rect().width*0.5:
			self.pos.x = window.get_rect().width*0.5
		elif self.pos.x < -window.get_rect().width*0.5:
			self.pos.x = -window.get_rect().width*0.5
		elif self.pos.y > window.get_rect().height*0.5:
			self.pos.y = window.get_rect().height*0.5
		elif self.pos.y < -window.get_rect().height*0.5:
			self.pos.y = -window.get_rect().height*0.5
