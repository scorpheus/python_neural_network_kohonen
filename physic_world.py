__author__ = 'scorpheus'

from Vec2D import Vec2d
import numpy as np
from random import randint
import math


class RandomSphereList():
	def __init__(self, window):
		self.sphere_array = np.array([])

		for id_sphere in range(150):
			vec = {'x': randint(-window.get_rect().width*0.5, window.get_rect().width*0.5), 'y': randint(-window.get_rect().height*0.5, window.get_rect().height*0.5), 'r': 5}
			self.sphere_array = np.append(self.sphere_array, [vec])

	def draw(self, pygame_draw, window):
		for pos_sphere in range(self.sphere_array.shape[0]):
			integer_pos = Vec2d(int(self.sphere_array[pos_sphere]['x']), int(self.sphere_array[pos_sphere]['y']))
			pygame_draw.circle(window, (255, 255, 255), integer_pos + window.get_rect().center, self.sphere_array[pos_sphere]['r'], 1)


class PhysicWorld():
	def __init__(self, window):
		self.sphere_list = RandomSphereList(window)

	def draw(self, pygame_draw, window):
		self.sphere_list.draw(pygame_draw, window)

	def intersection_line_spheres(self, s, d):
		min_intersection_d = 1000000
		for pos_sphere in range(self.sphere_list.sphere_array.shape[0]):
			temp_d = self.LineIntersectSphere(s, d, Vec2d(self.sphere_list.sphere_array[pos_sphere]['x'], self.sphere_list.sphere_array[pos_sphere]['y']), self.sphere_list.sphere_array[pos_sphere]['r'])
			if 0 < temp_d < min_intersection_d:
				min_intersection_d = temp_d
		return min_intersection_d

	def LineIntersectSphere(self, o, d, c, r):
		e = c - o

		k = e.dot(d)
		v = r * r - (e.get_length_sqrd() - k * k)
		if v < 0:
			return 1000000

		v = math.sqrt(v)

		return k - v
