#higher objects must come first

import os
import waveparticle
from waveparticle import *
import menu

def level0():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards", "vials"]
	width = 1400
	height = 800
	bg = "img" + os.sep + "bg0.png"
	block03 = RedBlock([(490, 0), (500, 240), (580, 320), (640, 320), (640, 0)])
	block04 = RedBlock([(640, 0), (640, 320), (700, 400), (800, 400), (900, 300), (900, 0)])
	block07 = RedBlock([(900, 0), (900, 300), (1400, 300), (1400, 0)])
	block08 = RedBlock([(995, 240), (1005, 500), (1400, 500), (1400, 240)])
	block09 = RedBlock([(0, 200), (0, 400), (200, 400), (180, 200)])
	block10 = RedBlock([(400, 320), (397, 400), (503, 400), (500, 320)])
	block11 = GlassBlock([(1100, 500), (1100, 580), (1200, 580), (1200, 500)])
	block12 = RedBlock([(1300, 500), (1300, 580), (1400, 580), (1400, 500)])
	block13 = RedBlock([(0, 400), (0, 800), (600, 800), (600, 400)])
	block14 = RedBlock([(600, 480), (600, 800), (900, 800), (900, 500), (860, 480)])
	block15 = RedBlock([(900, 580), (900, 800), (1400, 800), (1400, 580)])
	help1 = Helptext((240, 320), (320, 400), "Press A to move left\nPress D to move right")
	help2 = Helptext((320, 320), (400, 400), "Press W to jump\nPress W with A/D to jump left/right")
	help3 = Helptext((900, 500), (940, 580), "Hmm... A sheet of glass.\nWhat if I jump off the top of this ledge? I wonder...")
	hole = Hole((280, 320))
	wormhole = Wormhole((1260, 540))
	frontObj = [block03, block04, block07, block08, block09, block10,
				block11, block12, block13, block14, block15,
				help1, help2, help3]
	backObj = [hole]
	guards = []
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))

def level1():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards"]
	width = 2500
	height = 11900
	bg = "img" + os.sep + "bg1.png"
	block01 = RedBlock([(0, 11200), (0, 11900), (340, 11900), (340, 11400), (300, 11200)])
	block02 = RedBlock([(0, 11400), (0, 11900), (540, 11900), (540, 11600), (500, 11400)])
	block08 = RedBlock([(0, 11600), (0, 11900), (2500, 11900), (2500, 11600)])
	block07 = RedBlock([(700, 11600), (700, 11900), (2500, 11900), (2500, 11200), (780, 11200)])
	block06 = RedBlock([(900, 11200), (900, 11900), (1100, 11900), (1100, 11140), (920, 11140)])
	block03 = RedBlock([(1000, 11140), (1000, 11900), (1110, 11900), (1110, 11200), (1100, 11080), (1020, 11080)])
	block05 = RedBlock([(1000, 11200), (1000, 11900), (2500, 11900), (2500, 11200)])
	block04 = RedBlock([(1300, 11200), (1300, 11900), (2500, 11900), (2500, 11100), (1320, 11100)])
	help1 = Helptext((340, 11360), (500, 11400), "What was that?! It seems like I morphed into a light wave\nthat was barely affected by gravity.")
	help2 = Helptext((0, 0), (2500, 10500), "It seems like I've morphed again. I notice that this happens whenever I exceed a certain speed.\nI need to be careful. If I exceed the bounds of this map I'll disappear forever.\nPerhaps morphing back into a particle might help. Press W to morph.")
	help3 = Helptext((540, 11560), (570, 11600), "I'm stuck. Move to the mouse to the top left corner of the screen and click on the \"Restart\" button.")
	hole = Hole((380, 11340))
	wormhole = Wormhole((1205, 11140))
	frontObj = [block01, block02, block03, block04, block05, block06, block07, block08, help1, help2, help3]
	backObj = [hole]
	guards = []
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))

def level2():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards"]
	width = 2000
	height = 2000
	bg = "img" + os.sep + "bg2.png"
	block01 = BlackBlock([(330, 1200), (310, 1260), (350, 1300), (600, 1300), (640, 1260), (580, 1120), (540, 1100)])
	block02 = BlackBlock([(840, 1090), (800, 1150), (800, 1210), (1000, 1210), (1040, 1150), (960, 1050), (900, 1050), (880, 1090)])
	block03 = DarkRedBlock([(0, 1500), (0, 2000), (200, 2000), (150, 1500)])
	block04 = DarkRedBlock([(0, 1700), (0, 2000), (400, 2000), (400, 1700)])
	block05 = DarkRedBlock([(600, 1700), (600, 12000), (800, 2000), (800, 1700)])
	block06 = DarkRedBlock([(950, 1700), (950, 2000), (1200, 2000), (1200, 1700)])
	block07 = RedBlock([(1760, 1520), (1760, 2000), (1860, 2000), (1860, 1520), (1840, 1460), (1780, 1460)])
	block08 = RedBlock([(1600, 1600), (1600, 2000), (2000, 2000), (1900, 1520), (1640, 1520)])
	block09 = RedBlock([(1350, 1600), (1350, 2000), (1800, 2000), (1800, 1600)])
	help1 = Helptext((50, 1400), (150, 1550), "Ooh. It seems like I can stand on this dark red block.\nBut I guess I should be careful when transforming into a wave.\nThe black blocks would probably absorb me entirely, and the dark red ones, partially.")
	hole = Hole((100, 1450))
	vial1 = Vial((1800, 1400))
	wormhole = Wormhole((1920, 1360))
	frontObj = [block01, block02, block03, block04, block05, block06, block07, block08, block09, help1]
	backObj = [hole, vial1]
	guards = []
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))

def level3():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards"]
	width = 800
	height = 600
	bg = "img" + os.sep + "bg2.png"
	block01 = RedBlock([(100, 400), (100, 500), (700, 500), (700, 400)])
	guard1 = Guard((570, 370), [(570, 370), (400, 370)])
	guard2 = Guard((300, 370), [(300, 370), (400, 370), (350, 320)])
	help1 = Helptext((100, 350), (200, 400), "Those are guardians of the universe.\nThey can capture me in particle form.\nIn wave form, I can pass through them to deactivate it.")
	hole = Hole((150, 350))
	wormhole = Wormhole((650, 350))
	frontObj = [block01, help1]
	backObj = [hole]
	guards = [guard1, guard2]
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))

def level4():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards"]
	width = 800
	height = 1000
	bg = "img" + os.sep + "bg2.png"
	block01 = RedBlock([(0, 100), (0, 150), (600, 150), (600, 100)])
	block02 = GlassBlock([(500, 250), (500, 875), (625, 875), (750, 750), (750, 250)])
	block03 = RedBlock([(300, 850), (300, 900), (500, 900), (500, 850)])
	block04 = GlassBlock([(300, 500), (50, 500), (50, 700), (200, 875), (300, 875)])
	block05 = BlackBlock([(175, 200), (175, 300), (200, 325), (300, 325), (325, 250), (300, 175), (200, 175)])
	guard = Guard((625, 225), [(625, 225), (700, 225)])
	hole = Hole((50, 50))
	wormhole = Prisoner((460, 290))
	frontObj = [block01, block02, block05, block04, block03]
	backObj = [hole]
	guards = [guard]
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))


#==============================================================================

"""
HOW TO CREATE A LEVEL:

def leveln():
	gravity = (0, 3)
	keyList = ["wp", "width", "height", "bg", "backObj", "frontObj", "wormhole", "guards"]
	width = <whatever width you want for your game universe>
	height = <whatever height you want for your game universe>
	bg = <path to background image>
	<all objects you want to place in the map (optional)>
	Types of objects:
		BlackBlock([List of vertices in anti-clockwise order])
		DarkRedBlock([List of vertices in anti-clockwise order])
		RedBlock([List of vertices in anti-clockwise order])
		Helptext(topleft, bottomright, text)
		Vial(xy of center)
		Guard([starting coordinates, List of Coordinates along path])
	</all objects you want to place in the map (optional)>
	Hole(xy of center) #where player starts
	Wormhole(xy of center) #destination to clear level
	frontObj = [<list of all objects to be placed in front of player>]
	backObj = [<vials, Hole>]
	guards = [<list of all guards>]
	wp = Waveparticle(hole.P, (width, height), gravity)
	valList = [wp, width, height, bg, backObj, frontObj, wormhole, guards]
	return dict(zip(keyList, valList))
"""