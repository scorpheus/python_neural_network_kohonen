from math import cos, sin, pi
import gs
import gs.plus.render as render

step = 15
step_to_pi = 2*pi / step
cos_table = []
sin_table = []
for s in range(step):
	cos_table.append(cos(s * step_to_pi))
	sin_table.append(sin(s * step_to_pi))
cos_table.append(cos(0))
sin_table.append(sin(0))

def circle3d(x, y, r, color=gs.Color.White):
	"""Draw a 3d circle"""
	for s in range(step):
		render.line3d(x + cos_table[s] * r, 1.1, y + sin_table[s] * r, x + cos_table[s+1] * r, 1.1, y + sin_table[s+1] * r, color, color)
