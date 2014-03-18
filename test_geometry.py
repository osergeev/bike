
from geometry import *

def test_pointcreation():
	p = Point()
	p.setCoords(1, 2)
	assert p.getCoords() == (1, 2)

def test_pointConstructor():
	p = Point()
	assert p.getCoords() == (0, 0)
	p = Point(2, 3)
	assert p.getCoords() == (2, 3)

def test_pointDistance():
	p1 = Point(1, 2)
	p2 = Point(4, -2)
	assert dist(p1, p2) == 5.0

def test_comparison():
	p1 = Point(1, 2)
	p2 = Point(4, 3)
	assert p1 < p2
	assert p1 <= p2
	assert p2 > p1
	assert p2 >= p1
	assert p1 <= p1
	assert p2 >= p2
	l = [p2, p1]
	l.sort()
	assert l == [Point(1, 2), Point(4, 3)]