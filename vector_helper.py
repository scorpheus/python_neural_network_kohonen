from math import cos, sin, radians

def rotate(vec, angle_degrees):
	rad = radians(angle_degrees)
	c = cos(rad)
	s = sin(rad)
	x = vec.x*c - vec.y*s
	y = vec.x*s + vec.y*c
	vec.x = x
	vec.y = y
