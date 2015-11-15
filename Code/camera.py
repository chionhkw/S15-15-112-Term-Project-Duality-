import physics as p
import math as m

class Camera:

	def __init__(self, (camWidth, camHeight), (globalWidth, globalHeight), (camX, camY)):
		(self.camWidth, self.camHeight) = (camWidth, camHeight)
		(self.globalWidth, self.globalHeight) = (globalWidth, globalHeight)
		#ensure camera view does not move beyond the global view
		self.bound(camX, camY)

	def follow(self, other):
		partition = 4
		factor = 0.01
		allowance = 10
		Hooke = factor * p.dist((self.camX, self.camY), (other.x, other.y))
		#refocus on other if not moving
		if Hooke > allowance and (self.camX, self.camY) != (other.x, other.y):
			self.camX += (other.x - self.camX) / Hooke**2
			self.camY += (other.y - self.camY) / Hooke**2
			self.bound(self.camX, self.camY)
			return None
		#if moving but not going offscreen
		if (p.distX((self.camX, self.camY), (other.x, other.y)) < self.camWidth / partition and
			p.distY((self.camX, self.camY), (other.x, other.y)) < self.camHeight / partition):
			self.bound(self.camX, self.camY)
			return None
		#otherwise moving and going offscreen
		#follow x-dir
		if other.x > self.camX + self.camWidth / partition:
			self.camX = other.x - self.camWidth /partition
		elif other.x < self.camX - self.camWidth / partition:
			self.camX = other.x + self.camWidth / partition
		#follow y-dir
		if other.y > self.camY + self.camHeight / partition:
			self.camY = other.y - self.camHeight /partition
		elif other.y < self.camY - self.camHeight / partition:
			self.camY = other.y + self.camHeight / partition
		self.bound(self.camX, self.camY)
		return None

	def bound(self, x, y):
		self.camX = p.bound(x, self.camWidth / 2, self.globalWidth - self.camWidth / 2)
		self.camY = p.bound(y, self.camHeight / 2, self.globalHeight - self.camHeight / 2)

	def draw(self, canvas, objList):
		bg = True
		for obj in objList:
			if bg:
				speed = 1.2
				obj.draw(canvas, (speed * self.camX - self.camWidth / 2, self.camY - self.camHeight / 2))
				bg = False
				continue
			obj.draw(canvas, (self.camX - self.camWidth / 2, self.camY - self.camHeight / 2))