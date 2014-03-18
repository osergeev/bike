from math import *

class Point(object):
	def __init__(self):
		self._x = 0
		self._y = 0

	def get_coords(self):
		return (self._x, self._y)

	def set_coords(self, x, y):
		self._x = x
		self._y = y

def dist(p1, p2):
	xdiff = p2.get_coords[0] - p1.get_coords[0]
	ydiff = p2.get_coords[1] - p1.get_coords[1]
	return sqrt(xdiff*xdiff + ydiff*ydiff)

