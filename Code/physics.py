from math import *

def dist(P1, P2=(0, 0)):
	return distSq(P1, P2)**0.5

def distSq(P1, P2=(0, 0)):
	return distX(P1, P2)**2 + distY(P1, P2)**2

def distX((x1, y1), (x2, y2)):
	return abs(x1 - x2)

def distY((x1, y1), (x2, y2)):
	return abs(y1 - y2)

def fixNorm(P, d=1):
	if dist(P) == 0: return (0, 0)
	norm = d/dist(P)
	return sprod(P, norm)

def vadd(*args):
	sumX = 0
	sumY = 0
	for (x, y) in args:
		sumX += x
		sumY += y
	return (sumX, sumY)

def vsub((x1, y1), (x2, y2)):
	return (x1 - x2, y1 - y2)

def sprod((x, y), c):
	return (c*x, c*y)

def bound(x, x1, x2):
	return min(max(x, x1), x2)

def almostEq(a, b, delta=10**-5):
	return abs(a - b) < delta

def changeXComp((x, y), z=0):
	return (z, y)

def changeYComp((x, y), z=0):
	return (x, z)

def reflectX((x, y)):
	return (-x, y)

def reflectY((x, y)):
	return (x, -y)

def det(*args):
	summ = 0
	L = len(args)
	for i in xrange(L):
		summ += args[i][0] * ( args[(i + 1) % L][1] - args[(i - 1) % L][1] )
	return summ

def orthogonal((x, y)):
	return (-y, x)

def dot((x1, y1), (x2, y2)):
	return x1 * x2 + y1 * y2

def vangle((x, y)):
	if x == 0:
		if y > 0:
			return pi / 2
		else:
			return 3 * pi / 2
	else:
		return atan(1.0 * y / x)

def perPt(P, Q, R):
	base = vsub(Q, P)
	projV = proj(vsub(R, P), base)
	return vadd(P, projV)

def reflect(incidentV, surfaceV):
	# angle = 2 * vangle(surfaceV) - vangle(incidentV)
	# P = (math.cos(angle), math.sin(angle))
	# d = dist(incidentV)
	P = perPt((0, 0), surfaceV, incidentV)
	return vsub(sprod(P, 2), incidentV)

#http://en.wikipedia.org/wiki/Snell's_law#Vector_form
def refract(incidentV, surfaceV, n1, n2, errorMsg=True):
	l = fixNorm(incidentV)
	n = fixNorm(orthogonal(surfaceV))
	c = -dot(n, l)
	r = 1.0 * n1 / n2
	abomination = 1 - r**2 * (1 - c**2) 
	if abomination >= 0:
		return vadd(sprod(l, r), sprod(n, r * c - sqrt(abomination)))
	elif errorMsg:
		return False
	else:
		return reflect(incidentV, surfaceV)

def proj(a, n):
	return sprod(n, 1.0 * dot(a, n) / distSq(n))