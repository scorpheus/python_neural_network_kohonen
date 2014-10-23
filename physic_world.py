__author__ = 'scorpheus'

from simple_vec2d import SimpleVec2D
import numpy as np
from random import randint
import math


class sphere():
	def __init__(self, x, y, r, center):
		self.pos = SimpleVec2D(x, y)
		self.r = r
		self.d_pos = (int(self.pos.x)+center[0], int(self.pos.y)+center[1])


class RandomSphereList():
	def __init__(self, window):
		self.sphere_array = []

		for id_sphere in range(50):
			self.sphere_array.extend([sphere(randint(-window.get_rect().width*0.5, window.get_rect().width*0.5), randint(-window.get_rect().height*0.5, window.get_rect().height*0.5), 15, window.get_rect().center)])

	def draw(self, pygame_draw, window):
		for pos_sphere in self.sphere_array:
			pygame_draw.circle(window, (255, 255, 255), pos_sphere.d_pos, pos_sphere.r, 1)


class PhysicWorld():
	def __init__(self, window):
		self.sphere_list = RandomSphereList(window)

	def draw(self, pygame_draw, window):
		self.sphere_list.draw(pygame_draw, window)

	def in_collision_with_spheres(self, pos, r):
		max_dist_check = r**2
		for pos_sphere in self.sphere_list.sphere_array:
			if pos_sphere.pos.get_dist_sqrd(pos) <= max_dist_check+pos_sphere.r**2:
				return True
		return False

	def intersection_line_spheres(self, s, d, max_dist):
		min_intersection_d = 1000000
		max_dist_check = max_dist**2
		for pos_sphere in self.sphere_list.sphere_array:
			if pos_sphere.pos.get_dist_sqrd(s) < max_dist_check:
				temp_d = self.LineIntersectSphere(s, d, pos_sphere.pos, pos_sphere.r)
				if 0 < temp_d < min_intersection_d:
					min_intersection_d = temp_d
		return min_intersection_d

	e = SimpleVec2D(0, 0)
	def LineIntersectSphere(self, o, d, c, r):
		self.e.x = c.x
		self.e.y = c.y
		self.e -= o

		k = self.e.dot(d)
		v = r * r - (self.e.get_length_sqrd() - k * k)
		if v < 0:
			return 1000000

		v = math.sqrt(v)

		return k - v
