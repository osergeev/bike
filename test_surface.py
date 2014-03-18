
from geometry import *
from surface import *

def test_surface():
	p = Point(1, 1)
	p2 = Point(-1, 2)
	p3 = Point(8, -4)
	pb = Point(0, 0)
	pe = Point(4, 0)
	elem = SurfaceElement(pb, pe)
	assert elem.getClosestPoint(p) == Point(1, 0)
	assert elem.getClosestPoint(p2) == Point(0, 0)
	assert elem.getClosestPoint(p3) == Point(4, 0)
	elem2 = SurfaceElement(Point(4, 0), Point(7, -4))
	elem3 = SurfaceElement(Point(7, -4), Point(12, -4))
	elem4 = SurfaceElement(Point(12, -4), Point(15, 0))
	elem5 = SurfaceElement(Point(15, 0), Point(15, 3))
	surf = Surface(100, 50, [elem, elem2, elem3, elem4, elem5])
	p4 = Point(9.5, 0)
	closePoints = surf.getClosePoints(p4)
	print closePoints
