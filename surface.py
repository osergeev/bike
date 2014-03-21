from geometry import *
import numpy as np
import random as R

class SurfaceElement(object):
	"""An auxiliary class for constructing a surface
	and calculating distances."""
	def __init__(self, pb, pe):
		self._pb = pb
		self._pe = pe
		self._w = pe.x - pb.x
		self._h = pe.y - pb.y
		self._len = dist(self._pb, self._pe)

	def getW(self):
		"""Returns x projection of the element."""
		return self._w

	def getH(self):
		"""Returns y projection of the element."""
		return self._h

	def getLen(self):
		"""Returns length of the element."""
		return self._len

	def getBegin(self):
		"""Returns left point of the element."""
		return self._pb

	def getEnd(self):
		"""Returns right point of the element."""
		return self._pe

	def isAbove(self, p):
		"""True if a given point is above the element. 
		Used for masses."""
		x = p.x
		if x > self._pb.x and x < self._pe.x:
			y = p.y
			if y < self._pb.y + (self._h) * (x - self._pb.x) / (self._w):
				return True
		return False

	def getClosestPoint(self, p):
		"""Returns point of a segment, 
		closest to the given point."""
		if (p.x - self._pb.x) * self._h == (p.y - self._pb.y) * self._w:	#if p is on a line, a/b = c/d
			crossPoint = p
		else:
			a = np.array([[self._w, -self._h], [self._h, self._w]])
			b = np.array([p.x - self._pb.x, p.y - self._pb.y])
			x = np.linalg.solve(a, b)
			crossPoint = Point(self._pb.x + x[0] * self._w, self._pb.y + x[0] * self._h)

		if crossPoint.x < self._pb.x:
			return self._pb
		elif crossPoint.x > self._pe.x:
			return self._pe
		else:
			return crossPoint

class Surface(object):
	"""Represents a surface on which bicycle moves.
	It is created randomly and once for the whole process."""
	def __init__(self, distance, height, elems=[]):
		if len(elems) > 0:
			self._elements = elems
			self._pts = []
			self._distance = distance
			self._height = height
			for e in elems:
				self._pts.append(e.getBegin())
			self._pts.append(e.getEnd())
		else:
			self._pts = [Point(0, 0), Point(5, 0)]
			self._elements = [SurfaceElement(self._pts[0], self._pts[1])]
			currPoint = self._pts[1]
			self._distance = distance
			self._height = 0
			while currPoint.x < distance:
				w = 0.5 + R.random() * 2.5
				if currPoint.x + w > distance:
					w = distance - currPoint.x + 5
					h = 0
				else:
					h = (2 * R.random() - 1) * w * 0.7
					self._height += h
					if self._height > height:
						h = -h
						self._height += 2 * h
					if self._height < -height:
						h = -h
						self._height += 2 * h
				nextPoint = Point(currPoint.x + w, currPoint.y + h)
				self._elements.append(SurfaceElement(currPoint, nextPoint))
				self._pts.append(nextPoint)
				currPoint = nextPoint

	def getDistance(self):
		"""Returns surface length along x direction."""
		return self._distance

	def getHeight(self):
		"""Returns surface length along y direction."""
		return self._height

	def getPoints(self):	# use for visualization
		"""Returns all consituent points"""
		return self._pts

	def isAbove(self, p):	# use with masses
		"""Tris function returns True if the surface is above
		the given point. Used for masses."""
		for e in self._elements:
			if e.isAbove(p):
				return True
		return False

	def getClosePoints(self, p):	# use with wheels
		"""Returns list of the surface points
		closest to the given point, sorted from the
		rightmost point to the leftmost one. Used for wheels."""
		cpts = []
		distances = {}
		for e in self._elements:
			if dist(p, e.getBegin()) > 20:
				continue
			cpt = e.getClosestPoint(p)
			distance = dist(p, cpt)
			distances.setdefault(distance, [])	# only creates an empty list if it doesn't exist
			distances[distance].append(cpt)
		mindist = min(distances)
		keys = distances.keys()
		chosenkeys = [x for x in keys if x < 1.2 * mindist]
		distances = {x: distances[x] for x in chosenkeys}
		for d in distances:
			cpts = cpts + distances[d]
		cpts.sort(reverse = True)
		return cpts
