from math import *

class Point(object):
	def __init__(self, x=0, y=0):
		self._x = float(x)
		self._y = float(y)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, value):
		self._y = value

	def getCoords(self):
		return (self._x, self._y)

	def setCoords(self, x, y):
		self._x = x
		self._y = y

	def __le__(self, other):
		if self.x <= other.x:
			return True
		return False

	def __ge__(self, other):
		if self.x >= other.x:
			return True
		return False

	def __lt__(self, other):
		if self.x < other.x:
			return True
		return False

	def __gt__(self, other):
		if self.x > other.x:
			return True
		return False

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		return False

def dist(p1, p2):
	xdiff = p2.x - p1.x
	ydiff = p2.y - p1.y
	return sqrt(xdiff*xdiff + ydiff*ydiff)


