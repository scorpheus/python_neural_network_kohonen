import math

class SimpleVec2D():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def rotate(self, angle_degrees):
		radians = math.radians(angle_degrees)
		cos = math.cos(radians)
		sin = math.sin(radians)
		x = self.x*cos - self.y*sin
		y = self.x*sin + self.y*cos
		self.x = x
		self.y = y

	# vectory functions
	def get_length_sqrd(self):
		return self.x**2 + self.y**2

	def get_length(self):
		return math.sqrt(self.x**2 + self.y**2)

	def __setlength(self, value):
		length = self.get_length()
		self.x *= value/length
		self.y *= value/length
	length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

	def dot(self, other):
		return float(self.x*other.x + self.y*other.y)

	def get_distance(self, other):
		return math.sqrt((self.x - other.y)**2 + (self.y - other.y)**2)

	def get_dist_sqrd(self, other):
		return (self.x - other.y)**2 + (self.y - other.y)**2

	# Addition
	def __add__(self, other):
		if isinstance(other, SimpleVec2D):
			return SimpleVec2D(self.x + other.x, self.y + other.y)
		elif hasattr(other, "__getitem__"):
			return SimpleVec2D(self.x + other[0], self.y + other[1])
		else:
			return SimpleVec2D(self.x + other, self.y + other)
	__radd__ = __add__
	
	# Subtraction
	def __sub__(self, other):
		if isinstance(other, SimpleVec2D):
			return SimpleVec2D(self.x - other.x, self.y - other.y)
		elif (hasattr(other, "__getitem__")):
			return SimpleVec2D(self.x - other[0], self.y - other[1])
		else:
			return SimpleVec2D(self.x - other, self.y - other)
	def __rsub__(self, other):
		if isinstance(other, SimpleVec2D):
			return SimpleVec2D(other.x - self.x, other.y - self.y)
		if (hasattr(other, "__getitem__")):
			return SimpleVec2D(other[0] - self.x, other[1] - self.y)
		else:
			return SimpleVec2D(other - self.x, other - self.y)
	def __isub__(self, other):
		if isinstance(other, SimpleVec2D):
			self.x -= other.x
			self.y -= other.y
		elif (hasattr(other, "__getitem__")):
			self.x -= other[0]
			self.y -= other[1]
		else:
			self.x -= other
			self.y -= other
		return self
 
	# Multiplication
	def __mul__(self, other):
		if isinstance(other, SimpleVec2D):
			return SimpleVec2D(self.x*other.x, self.y*other.y)
		if (hasattr(other, "__getitem__")):
			return SimpleVec2D(self.x*other[0], self.y*other[1])
		else:
			return SimpleVec2D(self.x*other, self.y*other)
	__rmul__ = __mul__
 
	def __imul__(self, other):
		if isinstance(other, SimpleVec2D):
			self.x *= other.x
			self.y *= other.y
		elif (hasattr(other, "__getitem__")):
			self.x *= other[0]
			self.y *= other[1]
		else:
			self.x *= other
			self.y *= other
		return self
 
	# Division
	def __div__(self, other):
		if isinstance(other, SimpleVec2D):
			return SimpleVec2D(self.x/other.x, self.y/other.y)
		if (hasattr(other, "__getitem__")):
			return SimpleVec2D(self.x/other[0], self.y/other[1])
		else:
			return SimpleVec2D(self.x/other, self.y/other)
	__rdiv__ = __mul__
 
	def __idiv__(self, other):
		if isinstance(other, SimpleVec2D):
			self.x /= other.x
			self.y /= other.y
		elif (hasattr(other, "__getitem__")):
			self.x /= other[0]
			self.y /= other[1]
		else:
			self.x /= other
			self.y /= other
		return self

	def __len__(self):
		return 2

	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError("Invalid subscript "+str(key)+" to Vec2d")