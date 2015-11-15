from Tkinter import *
from PIL import Image, ImageTk
import os
import physics as p


class Menu():
	def __init__(self, width, height):
		root = "img" + os.sep
		#background============================================================
		self.bg = Image.open(root + "bg.png")
		(x, y) = self.bg.size
		wPercent = 1.0 * width / x
		hPercent = 1.0 * height / y
		resizePercent = max(wPercent, hPercent)
		self.bg = self.bg.resize((int(x * resizePercent) + 1, int(y * resizePercent) + 1), Image.ANTIALIAS)
		self.bg = ImageTk.PhotoImage(self.bg)
		#buttons===============================================================
		self.midX = width / 2
		self.midY = height / 2
		self.buttonsOff = []
		self.buttonsOn = []
		self.buttonHeight = 50
		for imgName in ["solarsystem", "interstellar", "galaxy", "universe", "beyond"]:
			self.buttonsOff.append(openImg(root + "level_" + imgName + ".png"))
			self.buttonsOn.append(openImg(root + "level_" + imgName + "_selected.png"))
		self.selected = None

	def updateMove(self, move):
		self.selected = None
		(x, y) = move
		if abs(self.midY - y) > 125 or abs(self.midX - x) > 100: return None
		for i in xrange(-2, 3):
			imgY = self.midY + 50 * i
			if imgY - 25 < y < imgY + 25 and self.midX - 100 < x < self.midX + 100:
				self.selected = (i + 2, imgY)

	def updateClick(self, click):
		(x, y) = click
		if abs(self.midY - y) > 125 or abs(self.midX - x) > 100: return None
		return (y - (self.midY - 125)) / 50

	def draw(self, canvas):
		canvas.create_image(0, 0, anchor=NW, image=self.bg)
		for i in xrange(len(self.buttonsOff)):
			canvas.create_image(self.midX, self.midY + 50 * (i - 2), image=self.buttonsOff[i])
		if self.selected != None:
			canvas.create_image(self.midX, self.selected[1], image=self.buttonsOn[self.selected[0]])


class SideMenu():
	def __init__(self):
		root = "img" + os.sep
		self.pause = openImg(root + "pause.png")
		self.icon_menu = openImg(root + "icon_menu.png")
		self.icon_restart = openImg(root + "icon_restart.png")
		self.icon_volon = openImg(root + "icon_volon.png")
		self.icon_voloff = openImg(root + "icon_voloff.png")
		self.icon_selected = openImg(root + "icon_selected.png")
		self.icon_help = openImg(root + "icon_help.png")
		self.helpbox = openImg(root + "help.png")
		self.menuPos = (143, 41)
		self.restartPos = (41, 143)
		self.helpPos = (135, 96)
		self.volPos = (96, 135)
		self.vols = [self.icon_voloff, self.icon_volon]
		self.volCtrl = 1
		self.selected = None
		self.help = False
		
	def draw(self, canvas):
		canvas.create_image(55, 55, image=self.pause)
		if self.selected != None:
			canvas.create_image(self.selected, image=self.icon_selected)
		canvas.create_image(self.menuPos, image=self.icon_menu)
		canvas.create_image(self.restartPos, image=self.icon_restart)
		canvas.create_image(self.volPos, image=self.vols[self.volCtrl])
		canvas.create_image(self.helpPos, image=self.icon_help)
		if self.help:
			canvas.create_image(200, 200, anchor=NW, image=self.helpbox)

	def updateClick(self, click):
		if p.dist(self.menuPos, click) <= 25:
			return "menu"
		elif p.dist(self.restartPos, click) <= 25:
			return "restart"
		elif p.dist(self.volPos, click) <= 25:
			self.volCtrl = 1 - self.volCtrl
			return "volToggle"

	def updateMove(self, move):
		self.selected = None
		for loc in [self.menuPos, self.restartPos, self.volPos]:
			if p.dist(move, loc) <= 25:
				self.selected = loc
				break
		if p.dist(move, self.helpPos) <= 25:
			self.help = True
		else:
			self.help = False

class BG():
	def __init__(self, image):
		self.img = ImageTk.PhotoImage(Image.open(image))

	def draw(self, canvas, (topX, topY)):
		canvas.create_image(-topX, -topY, anchor=NW, image=self.img)

class Healthbar():
	def __init__(self, width, height):
		self.val = 66
		self.midX = width / 2
		self.midY = 40
		self.r = 15
		self.color = "red"
		self.outlineColor = "gray"

	def draw(self, canvas):
		if self.val > 0:
			canvas.create_arc(self.midX - 200 - self.r, self.midY - self.r,
							  self.midX - 200 + self.r, self.midY + self.r,
							  start=90, extent=180,
							  fill=self.color, outline=self.color,
							  width=3, style=PIESLICE)
			canvas.create_rectangle(self.midX - 200, self.midY - self.r,
									self.midX - 200 + 4 * self.val, self.midY + self.r,
									fill=self.color, outline=self.color)
		if self.val == 100:
			canvas.create_arc(self.midX + 200 - self.r, self.midY - self.r,
							  self.midX + 200 + self.r, self.midY + self.r,
							  start=-90, extent=180,
							  fill=self.color, outline=self.color,
							  width=3, style=PIESLICE)
		#draw the outlinebar
		canvas.create_arc(self.midX - 200 - self.r, self.midY - self.r,
						  self.midX - 200 + self.r, self.midY + self.r,
						  start=90, extent=180,
						  fill=self.color, outline=self.outlineColor,
						  width=3, style=ARC)
		canvas.create_arc(self.midX + 200 - self.r, self.midY - self.r,
						  self.midX + 200 + self.r, self.midY + self.r,
						  start=-90, extent=180,
						  fill=self.color, outline=self.outlineColor,
						  width=3, style=ARC)
		canvas.create_line(self.midX - 200, self.midY - self.r,
						   self.midX + 200, self.midY - self.r,
						   fill=self.outlineColor, width=3)
		canvas.create_line(self.midX - 200, self.midY + self.r,
						   self.midX + 200, self.midY + self.r,
						   fill=self.outlineColor, width=3)
		
	def update(self, wp):
		self.val = max(wp.health, 0)

def openImg(image):
	return ImageTk.PhotoImage(Image.open(image))