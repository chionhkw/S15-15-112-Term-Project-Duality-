from Tkinter import *
import physics as p
import time
from PIL import Image, ImageTk
import os
import subprocess
import copy

#Waveparticle class============================================================

class Waveparticle():
	def __init__(self, (x, y), (globX, globY), gravity):
		#particle/wave form
		self.isParticle = True
		#position
		self.x, self.y = x, y
		#velocity
		self.v = (0, 0)
		#radius
		self.r = 20
		#health
		self.health = 100
		self.maxHealth = 100
		self.mhu = 20	#minimum health unit
		#maximum speed before turning into wave
		self.maxSpeed = 35
		self.maxJump = 20
		self.maxImpulse = 10
		self.minImpulse = 2
		#collision with blocks
		self.collision = False
		#gravity experienced in particle form
		self.gravity = self.g = gravity
		#bounds of universe
		self.width = globX
		self.height = globY
		self.path = os.path.dirname(__file__)
		#particle images
		self.imgL = [openImg("img" + os.sep + "wp_left_%d.png" % i) for i in xrange(6)]
		self.imgR = [openImg("img" + os.sep + "wp_right_%d.png" % i) for i in xrange(6)]
		#initial image
		self.img = self.imgR
		#wave images
		self.imgList = [[openImg("img" + os.sep + "wave%d%d.png" % (i, j)) for j in xrange(4)] for i in xrange(6)]
		#list of positions for ray in wave form
		self.posList = None
		self.mrl = 20	#maximum ray length

	#for OnStep================================================================

	def update(self):
		#if not in universe
		if not (0 < self.x < self.width and 0 < self.y < self.height):
			self.health = 0
		#check health
		if self.health == 0:
			#play death sound
			subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "death.py"])
		self.health = self.health / self.mhu * self.mhu
		if self.isParticle:
			#no wave positions
			self.posList = None
			#velocity affected by gravity
			self.v = p.vadd(self.v, self.g)
			if p.dist(self.v) >= self.maxSpeed:
				#then transform to wave
				self.isParticle = False
				self.r = 12
				self.g = (0, 0)
				self.v = p.fixNorm(self.v, self.maxSpeed)
			if not self.collision:
				#gravity has effect
				self.g = self.gravity
			#select image to draw
		#select particle image
		if self.v[0] < 0:
			self.img = self.imgL
		elif self.v[0] > 0:
			self.img = self.imgR
		#change position
		(self.x, self.y) = p.vadd((self.x, self.y), self.v)
		if not self.isParticle:
			#then draw ray
			if self.posList == None:
				self.posList = [(self.x, self.y)]
			else:
				self.posList.append(p.vadd(p.sprod(self.posList[-1], 2/3.0), p.sprod((self.x, self.y), 1/3.0)))
				self.posList.append(p.sprod(p.vadd(self.posList[-1], (self.x, self.y)), 0.5))
				self.posList.append((self.x, self.y))
				while len(self.posList) > self.mrl:
					del self.posList[0: 3]
		
	#for OnDraw================================================================

	def draw(self, canvas, (topX, topY)):
		if self.isParticle:
			canvas.create_image(self.x - topX,
								self.y - topY,
								image=self.img[self.health / self.mhu])
		else:
			for i in xrange(len(self.posList)):
				image = self.imgList[self.health / self.mhu][min(i, 3)]
				canvas.create_image(self.posList[-i - 1][0] - topX,
									self.posList[-i - 1][1] - topY,
									image=image)

	#for OnKey=================================================================

	def transform(self):
		if self.collision:
			#not allowed to transform on collision
			return None
		self.isParticle = True
		self.r = 20
		self.g = self.gravity

	def move_up(self):
		if not self.collision:
			#cannot jump in the air
			return False
		subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "jump.py"])
		(P, Q) = self.collision
		(x, y) = p.vsub(Q, P)
		if self.collision and x <= 0 and abs(x) >= abs(y):
			#surface angle leq 45, can jump
			impDir = p.orthogonal((x, y))
			self.v = p.vadd(self.v, p.fixNorm(impDir, self.maxJump))
			self.collision = False
		return True

	def move_left(self):
		if not self.collision:
			#cannot change dir in the air
			return None
		(P, Q) = self.collision
		(x, y) = p.vsub(Q, P)
		if self.collision and x <= 0:
			if abs(x) >= abs(y):
				#surface angle leq 45, can move normally
				self.v = p.proj((-self.maxImpulse, 0),
								p.vsub(self.collision[1], self.collision[0]))
			else:
				#surface angle > 45, cannot move easily
				self.v = (-self.minImpulse, 0)

	def move_right(self):
		if not self.collision:
			#cannot change dir in the air
			return None
		(P, Q) = self.collision
		(x, y) = p.vsub(Q, P)
		if self.collision and x <= 0:
			if abs(x) >= abs(y):
				#surface angle leq 45, can move normally
				self.v = p.proj((self.maxImpulse, 0),
								p.vsub(self.collision[1], self.collision[0]))
			else:
				#surface angle > 45, cannot move easily
				self.v = (self.minImpulse, 0)

#Block class===================================================================

class Block():
	def __init__(self, ListOfCoordinates):
		pass

	def commonInit(self, ListOfCoordinates, color):
		self.path = os.path.dirname(__file__)
		self.LoC = ListOfCoordinates
		#bounding box for self
		(self.minX, self.minY) = (self.maxX, self.maxY) = self.LoC[0]
		for (x, y) in self.LoC:
			self.minX = min(self.minX, x)
			self.maxX = max(self.maxX, x)
			self.minY = min(self.minY, y)
			self.maxY = max(self.maxY, y)
		#create block shape with tiles
		img = blockCreate(self.LoC, color)
		self.img = ImageTk.PhotoImage(img)

	#collision checks==========================================================

	def collision(self, wp):
		if not (self.minX - wp.r <= wp.x <= self.maxX + wp.r
				and self.minY - wp.r <= wp.y <= self.maxY + wp.r):
			#then nowhere near block
			return False
		#check each individual side
		for i in xrange(len(self.LoC)):
			if self.checkEdgeCollision(wp, i):
				return True
		for i in xrange(len(self.LoC)):
			if self.checkVertexCollision(wp, i):
				return True
		return False

	def checkVertexCollision(self, wp, i):
		epsilon = 2
		P = self.LoC[i]
		R = (wp.x, wp.y)
		# check vertex collision with P
		checkDist = p.dist(P, R) <= wp.r + epsilon
		if checkDist:
			#move particle back to proper location
			self.calibrateParticleVertex(wp, P, R)
			L = len(self.LoC)
			Q = self.LoC[(i + 1) % L]
			S = self.LoC[(i - 1) % L]
			u = p.fixNorm(p.vsub(Q, P))
			v = p.fixNorm(p.vsub(P, S))
			w = p.vadd(u, v)
			if wp.isParticle:
				self.particleVertexCollision(wp, P)
			else:
				self.waveVertexCollision(wp, w)
			wp.collision = ((0, 0), w)

	def particleVertexCollision(self, wp, P):
		R = (wp.x, wp.y)
		if p.vsub(R, P)[1] <= 0:
			wp.g = p.proj(wp.gravity, p.vsub(R, P))

	def calibrateParticleVertex(self, wp, P, R):
		(wp.x, wp.y) = p.vadd(P, p.fixNorm(p.vsub(R, P), wp.r))

	def waveVertexCollision(self, wp, P, Q, S):
		#subclassed
		pass
		
	def checkEdgeCollision(self, wp, i):
		epsilon = 2
		P = self.LoC[i]
		Q = self.LoC[(i + 1) % len(self.LoC)]
		R = (wp.x, wp.y)
		nextR = p.vadd(R, wp.v)
		det = p.det(P, Q, R)
		d = p.dist(P, Q)
		# check edge collision
		checkDist = (d * (wp.r - wp.maxSpeed - epsilon) <= det <= d * (wp.r + epsilon))
		checkAngle1 = (p.distSq(P, Q) + p.distSq(Q, R) - p.distSq(P, R)) / p.dist(P, Q) / p.dist(Q, R) > 0
		checkAngle2 = (p.distSq(P, Q) + p.distSq(P, R) - p.distSq(Q, R)) / p.dist(P, Q) / p.dist(P, R) > 0
		checkDir = p.det(P, Q, R) + epsilon >= p.det(P, Q, nextR)
		if checkDist and checkAngle1 and checkAngle2 and checkDir:
			#move particle back to proper location
			self.calibrateParticleEdge(wp, P, Q, R)
			#calculate new velocity/gravity
			if wp.isParticle:
				self.particleEdgeCollision(wp, P, Q)
			else:
				self.waveEdgeCollision(wp, P, Q)
			wp.collision = (P, Q)
			return True

	def waveEdgeCollision(self, wp, P, Q, R):
		pass

	def particleEdgeCollision(self, wp, P, Q):
		wp.v = (0, 0)
		if p.vsub(Q, P)[0] <= 0:
			#then collided from the top
			wp.g = p.proj(wp.gravity, p.vsub(Q, P))

	#for particle collisions
	def calibrateParticleEdge(self, wp, P, Q, R):
		base = p.vsub(Q, P)
		perPt = p.perPt(P, Q, R)
		#ensure particle not in wall
		(wp.x, wp.y) = p.vadd(perPt, p.fixNorm(p.orthogonal(base), wp.r))

	#for OnDraw================================================================

	def draw(self, canvas, topCorner):
		canvas.create_image(self.minX - topCorner[0], self.minY - topCorner[1],
							anchor=NW, image=self.img)

#DarkRedBlock class============================================================

class DarkRedBlock(Block):
	def __init__(self, ListOfCoordinates): #anticlockwise order
		self.commonInit(ListOfCoordinates, "dark")

	def waveEdgeCollision(self, wp, P, Q):
		subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "ouch.py"])
		wp.v = p.reflect(wp.v, p.vsub(Q, P))
		wp.health -= 1

	def waveVertexCollision(self, wp, w):
		subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "ouch.py"])
		wp.v = p.reflect(wp.v, w)
		wp.health -= 1

#RedBlock class================================================================

class RedBlock(Block):
	def __init__(self, ListOfCoordinates): #anticlockwise order
		self.commonInit(ListOfCoordinates, "red")

	def waveEdgeCollision(self, wp, P, Q):
		subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "twang.py"])
		wp.v = p.reflect(wp.v, p.vsub(Q, P))

	def waveVertexCollision(self, wp, w):
		subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "twang.py"])
		wp.v = p.reflect(wp.v, w)

#BlackBlock class==============================================================

class BlackBlock(Block):
	def __init__(self, ListOfCoordinates): #anticlockwise order
			self.commonInit(ListOfCoordinates, "black")

	def waveEdgeCollision(self, wp, P, Q):
		wp.v = (0, 0)
		wp.g = (0, 0) #possibly already set
		wp.health = 0

	def waveVertexCollision(self, wp, w):
		wp.v = p.reflect(wp.v, w)
		wp.health = 0

#GlassBlock class==============================================================

class GlassBlock(Block):
	def __init__(self, ListOfCoordinates): #anticlockwise order
		self.commonInit(ListOfCoordinates, "glass")
		self.rIndex = 1.7
		self.inMe = False

	def waveEdgeCollision(self, wp, P, Q):
		wp.v = p.fixNorm(p.refract(wp.v, p.vsub(Q, P), 1, self.rIndex), wp.maxSpeed)
		wp.g = (0, 0)
		self.inMe = True

	def waveVertexCollision(self, wp, P):
		self.inMe = True

	def collision(self, wp):
		#check if in bounding box
		if not (self.minX - wp.r <= wp.x <= self.maxX + wp.r and self.minY - wp.r <= wp.y <= self.maxY + wp.r):
			return False
		epsilon = 2
		L = len(self.LoC)
		if self.inMe:
			inside = True	#still inside
			for i in xrange(L):
				P = self.LoC[i]
				Q = self.LoC[(i + 1) % L]
				R = (wp.x, wp.y)
				nextR = p.vadd((wp.x, wp.y), wp.v)
				det = p.det(P, Q, nextR)
				#if moving away from wall, continue
				if p.det(P, Q, R) >= det: continue
				inside &= (det <= p.dist(P, Q) * (epsilon - wp.r))
				if not inside: break #to retain values of P, Q
			if inside:
				return True #because collision
			#otherwise  check for internal reflection
			base = p.vsub(Q, P)
			if not p.refract(wp.v, base, self.rIndex, 1):
				wp.v = p.reflect(wp.v, base)
				return True
			#otherwise if not complete exit, return collision true
			if det < p.dist(P, Q) * wp.r:
				return True
			#otherwise complete exit, change angle
			self.inMe = False
			wp.v = p.fixNorm(p.refract(wp.v, p.vsub((0, 0), base), self.rIndex, 1), wp.maxSpeed)
			return False
		else:
			#check each individual side
			for i in xrange(L):
				if self.checkEdgeCollision(wp, i):
					return True
			for i in xrange(L):
				if self.checkVertexCollision(wp, i):
					return True
			return False

	def exitMe(self, wp, i):
		epsilon = 2
		P = self.LoC[i]
		Q = self.LoC[(i + 1) % len(self.LoC)]
		R = (wp.x, wp.y)
		nextR = p.vadd(R, wp.v)
		det = p.det(P, Q, R)
		d = p.dist(P, Q)
		# check edge collision
		checkDist = (d * (wp.r - wp.maxSpeed - epsilon) <= det <= d * (wp.r + epsilon))

	def calibrateParticleVertex(self, wp, P, R):
		pass

	def calibrateParticleEdge(self, wp, P, Q, R):
		if wp.isParticle:
			base = p.vsub(Q, P)
			perPt = p.perPt(P, Q, R)
			#ensure particle not in wall
			(wp.x, wp.y) = p.vadd(perPt, p.fixNorm(p.orthogonal(base), wp.r))

#Vial class====================================================================

class Vial():
	def __init__(self, (x, y)):
		self.r = 20
		self.lit = True
		self.P = (x, y)
		#load images
		self.imgF = openImg("img" + os.sep + "vial_full.png")
		self.imgE = openImg("img" + os.sep + "vial_empty.png")
		self.img = self.imgF

	def collision(self, wp):
		if not self.lit: return False
		if p.dist(self.P, (wp.x, wp.y)) < 20:
			heal = 40
			wp.health = min(wp.health + heal, wp.maxHealth)
			self.img = self.imgE
			self.lit = False
		return False

	def draw(self, canvas, topCorner):
		(x, y) = p.vsub(self.P, topCorner)
		canvas.create_image(x, y, image=self.img)

#hole class====================================================================

class Hole():
	def __init__(self, P):
		self.P = P
		self.loadImg()
		self.path = os.path.dirname(__file__)

	def loadImg(self):
		self.img = openImg("img" + os.sep + "hole.png")

	def complete(self, wp):
		return False

	def collision(self, wp): #allow self to be in objList
		return False

	def draw(self, canvas, topCorner):
		canvas.create_image(p.vsub(self.P, topCorner), image=self.img)

#Wormhole class================================================================

class Wormhole(Hole):
	def complete(self, wp):
		dist = 25
		if p.dist(self.P, (wp.x, wp.y)) <= dist:
			subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "end.py"])
			return True
		return False

	def loadImg(self):
		self.img = openImg("img" + os.sep + "wormhole.png")

class Prisoner(Wormhole):
	def loadImg(self):
		self.img = openImg("img" + os.sep + "prisoner.png")

#helptext class================================================================

class Helptext():
	def __init__(self, NWCorner, SECorner, text):
		(self.xMin, self.yMin) = NWCorner
		(self.xMax, self.yMax) = SECorner
		self.text = text
		self.display = False

	def collision(self, wp):
		self.display = (self.xMin < wp.x < self.xMax and self.yMin < wp.y < self.yMax)
		return False	#collision does not affect WP

	def draw(self, canvas, topCorner):
		if self.display:
			canvas.create_text(100, 100, text=self.text,
							   anchor=NW, font="Arial 12 bold", fill="white")

#enemy class===================================================================

class Guard():
	def __init__(self, P, pathList):
		self.L = len(pathList)
		self.index = 0
		self.P = P	#xy-position
		self.stride = 5
		self.r = 25
		self.pathList = pathList
		self.target = self.pathList[self.index]
		self.imgActive = [openImg("img" + os.sep + "guard_active%d.png" % i) for i in xrange(2)]
		self.imgInactive = [openImg("img" + os.sep + "guard_inactive%d.png" % i) for i in xrange(2)]
		self.img = self.imgActive
		self.imgDir = 0
		self.isActive = True

	def update(self):
		if not self.isActive:
			return None
		if p.dist(self.P, self.pathList[self.index]) < 2:
			#then near this position, guard moves towards next target
			self.index = (self.index + 1) % self.L
			self.target = self.pathList[self.index]
		dist = p.dist(self.P, self.target)
		direction = p.vsub(self.target, self.P)
		if direction[0] < 0:
			self.imgDir = 0
		elif direction[0] > 0:
			self.imgDir = 1
		move = p.fixNorm(direction, min(self.stride, dist))
		self.P = p.vadd(self.P, move)

	def draw(self, canvas, topCorner):
		(x, y) = self.P
		canvas.create_image(p.vsub(self.P, topCorner), image=self.img[self.imgDir])

	def collision(self, wp):
		if not self.isActive: return False
		if wp.isParticle and p.dist(self.P, (wp.x, wp.y)) < self.r + wp.r:
			wp.health = 0
		elif not wp.isParticle and p.dist(self.P, (wp.x, wp.y)) < self.r + wp.r:
			self.isActive = False
			self.img = self.imgInactive
		return False #collision with this does not constitute collision w block


#==============================================================================

#creates block at LoC of the specified color
def blockCreate(LoC, color):
	#initialize fill
	fill = Image.open("img" + os.sep + "block_%s.png" % color)
	fillX, fillY = fill.size
	fillL = fill.load()
	#initialize LoC
	L = len(LoC)
	minX, minY = maxX, maxY = LoC[0]
	for (x, y) in LoC:
		minX = min(minX, x)
		maxX = max(maxX, x)
		minY = min(minY, y)
		maxY = max(maxY, y)
	#initialize block
	img = Image.new("RGBA", (maxX - minX, maxY - minY), (255, 255, 255, 255))
	imgL = img.load()
	for i in xrange(maxX - minX):
		for j in xrange(maxY - minY):
			r, g, b, alpha = fillL[(i + minX) % fillX, (j + minY) % fillY]
			for k in xrange(L):
				if p.det(LoC[k], LoC[(k + 1) % L], p.vadd((i, j), (minX, minY))) > 0:
					alpha = 0
					break
			imgL[i, j] = (r, g, b, alpha)
	return img

#opens image at imageLoc
def openImg(imageLoc):
	return ImageTk.PhotoImage(Image.open(imageLoc))