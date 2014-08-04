__author__ = 'scorpheus'

from Vec2D import Vec2d
import numpy as np
from random import randint
import math


class RandomSphereList():
	def __init__(self, window):
		self.sphere_array = np.array([])

		for id_sphere in range(50):
			vec = {'x': randint(-window.get_rect().width*0.5, window.get_rect().width*0.5), 'y': randint(-window.get_rect().height*0.5, window.get_rect().height*0.5)}
			self.sphere_array = np.append(self.sphere_array, [vec])

	def draw(self, pygame_draw, window):
		radius = 5
		for pos_sphere in range(self.sphere_array.shape[0]):
			integer_pos = Vec2d(int(self.sphere_array[pos_sphere]['x']), int(self.sphere_array[pos_sphere]['y']))
			pygame_draw.circle(window, (255, 255, 255), integer_pos + window.get_rect().center, radius, 1)


class PhysicWorld():
	def __init__(self, window):
		self.sphere_list = RandomSphereList(window)

	def draw(self, pygame_draw, window):
		self.sphere_list.draw(pygame_draw, window)

	def intersection_line_sphere(self, s, d):
			pass

	def LineIntersectSphere(self, a, v, c, r, t0, t1):
		e = c - a

		k = e.Dot(v)
		d = r * r - (e.Len2() - k * k)
		if d < 0:
			return 1000000

		d = math.sqrt(d)

		return k - d
