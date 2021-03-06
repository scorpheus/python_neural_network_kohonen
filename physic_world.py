__author__ = 'scorpheus'

import numpy as np
from random import randint
import math
import gs
from render_helper import circle3d
import gs.plus.render as render


class sphere():
	def __init__(self, x, y, r):
		self.pos = gs.Vector2(x, y)
		self.r = r


class RandomSphereList():
	def __init__(self, size_world):
		self.sphere_array = []
		self.tile_array = []

		with open("map.txt") as f:
			data = f.readlines()
			y = -5
			for d in data:
				x = -5
				for v in d:
					if v == 'X':
						self.sphere_array.extend([sphere(x, y, 0.5)])
					x += 1
				y += 1

		self.tile_ground = render.get_render_system().LoadGeometry("@core/res/tile_0.geo")
		self.wall_1m = render.get_render_system().LoadGeometry("@core/res/wall_1m_high.geo")
		self.wall_2m = render.get_render_system().LoadGeometry("@core/res/wall_2m_high.geo")

	def draw(self):
		width = render.get_renderer().GetCurrentOutputWindow().GetSize().x
		height = render.get_renderer().GetCurrentOutputWindow().GetSize().y
		center = gs.Vector2(width/2, height/2)

		for pos_sphere in self.sphere_array:
			render.geometry3d(pos_sphere.pos.x, 0, pos_sphere.pos.y, self.wall_1m)
			circle3d(pos_sphere.pos.x, pos_sphere.pos.y, pos_sphere.r)


class PhysicWorld():
	def __init__(self, size_world):
		self.sphere_list = RandomSphereList(size_world)

	def draw(self):
		self.sphere_list.draw()

	def in_collision_with_spheres(self, pos, r):
		max_dist_check = r**2
		for pos_sphere in self.sphere_list.sphere_array:
			if gs.Vector2.Dist2(pos_sphere.pos, pos) <= max_dist_check+pos_sphere.r**2:
				return True
		return False

	def intersection_line_spheres(self, s, d, max_dist):
		min_intersection_d = 1000000
		max_dist_check = max_dist**2
		for pos_sphere in self.sphere_list.sphere_array:
			if gs.Vector2.Dist2(pos_sphere.pos, s) < max_dist_check:
				temp_d = self.LineIntersectSphere(s, d, pos_sphere.pos, pos_sphere.r)
				if 0 < temp_d < min_intersection_d:
					min_intersection_d = temp_d
		return min_intersection_d

	e = gs.Vector2(0, 0)

	def LineIntersectSphere(self, o, d, c, r):
		self.e.x = c.x
		self.e.y = c.y
		self.e -= o

		k = self.e.Dot(d)
		v = r * r - (self.e.Len2() - k * k)
		if v < 0:
			return 1000000

		v = math.sqrt(v)

		return k - v
