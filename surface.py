
from geometry import *
import numpy as np
import random as R

class SurfaceElement(object):
	def __init__(self, pb, pe):
		self._pb = pb
		self._pe = pe
		self._w = pe.x - pb.x
		self._h = pe.y - pb.y
		self._len = dist(self._pb, self._pe)

	def getW(self):
		return self._w

	def getH(self):
		return self._h

	def getLen(self):
		return self._len

	def getBegin(self):
		return self._pb

	def getEnd(self):
		return self._pe

	def isAbove(self, p):
		self.x = p.x
		if self.x > self._pb.x and self.x < self._pe.x:
			self.y = p.y
			if self.y < self._pb.y + (self._h) * (self.x - self._pb.x) / (self._w):
				return True
		return False

	def getClosestPoint(self, p):
		if (p.x - self._pb.x) * self._h == (p.y - self._pb.y) * self._w:	#if p is on a line, a/b = c/d
			self.crossPoint = p
		else:
			self.a = np.array([[self._w, -self._h], [self._h, self._w]])
			self.b = np.array([p.x - self._pb.x, p.y - self._pb.y])
			self.x = np.linalg.solve(self.a, self.b)
			self.crossPoint = Point(self._pb.x + self.x[0] * self._w, self._pb.y + self.x[0] * self._h)

		if self.crossPoint.x < self._pb.x:
			return self._pb
		elif self.crossPoint.x > self._pe.x:
			return self._pe
		else:
			return self.crossPoint

class Surface(object):
	def __init__(self, distance, height, elems=[]):
		if len(elems) > 0:
			self._elements = elems
			self._pts = []
			for self.e in elems:
				self._pts.append(self.e.getBegin())
			self._pts.append(elems[len(elems) - 1].getEnd())
		else:
			self._pts = [Point(0, 0), Point(5, 0)]
			self._elements = [SurfaceElement(self._pts[0], self._pts[1])]
			self.currPoint = self._pts[1]
			while self.currPoint.x < distance:
				self.w = R.random()
				if self.currPoint.x + self.w > distance:
					self.w = distance - self.currPoint.x + 5
					self.h = 0
				else:
					self.h = (2 * R.random() - 1) * self.w * 1.2	#TODO: check for exceeding maximum height
				self.nextPoint = Point(self.currPoint.x + self.w, self.currPoint.y + self.h)
				self._elements.append(SurfaceElement(self.currPoint, self.nextPoint))
				self._pts.append(self.nextPoint)
				self.currPoint = self.nextPoint

	def getPoints(self):	# use for visualization
		return self._pts

	def isAbove(self, p):	# use with masses
		for self.e in self._elements:
			if self.e.isAbove(p):
				return True
		return False

	def getClosePoints(self, p):	# use with wheels
		self.cpts = []
		self.distances = {}
		for self.e in self._elements:
			if dist(p, self.e.getBegin()) > 10:
				continue
			self.cpt = self.e.getClosestPoint(p)
			self.dist = dist(p, self.cpt)
			self.distances.setdefault(self.dist, [])	# only creates an empty list if it doesn't exist
			self.distances[self.dist].append(self.cpt)
		self.mindist = min(self.distances)
		self.keys = self.distances.keys()
		self.chosenkeys = [x for x in self.keys if x < 1.2 * self.mindist]
		self.distances = {x: self.distances[x] for x in self.chosenkeys}
		for self.d in self.distances:
			self.cpts = self.cpts + self.distances[self.d]
		self.cpts.sort(reverse = True)
		return self.cpts
