#adapted from Bryan Oakley (http://goo.gl/QsKBfD)
#and Dr Kosbie's eventBasedAnimation (cs.cmu.edu/~112)
#http://www.kosbie.net/cmu/fall-10/15-110/koz/misc-demos/src/winsoundDemo.py

from Tkinter import *
import tkMessageBox
import time
import menu
import os
from waveparticle import *
import camera as c
import levels
import winsound
import time
import copy

class Duality():
    def __init__(self, width, height, fps):
        self.path = os.path.dirname(__file__)       #should be global...
        #window
        self.root = Tk()
        self.root.title("DUALITY")
        self.root.resizable(width=False, height=False)
        self.width, self.height = width, height
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        #game screens
        self.quit = False
        self.inMovie = False
        self.inMenu = True
        self.inLevel = False
        self.inSideMenu = False
        self.inCredits = False
        #sounds
        self.sounding = False
        #settings
        self.fps = fps
        self.vol = True
        #game level
        self.level = 0
        self.Levels = [levels.level0, levels.level1, levels.level2, levels.level3, levels.level4]
        self.maxLevel = len(self.Levels) - 1
        #game menus
        self.sideMenu = menu.SideMenu()
        self.Menu = menu.Menu(self.width, self.height)
        self.Loading = menu.BG("img" + os.sep + "loading.png")
        #self.Healthbar = menu.Healthbar(self.width, self.height)
        #controls
        self.pressed = {}
        self._set_bindings()
    
    #controls==================================================================
    def _set_bindings(self):
        for char in ["w", "a", "d", "r"]:
            self.root.bind("<KeyPress-%s>" % char, self._pressed)
            self.root.bind("<KeyRelease-%s>" % char, self._released)
            self.pressed[char] = False
        self.root.bind("<ButtonRelease-1>", self._click)
        self.root.bind("<Motion>", self._move)

    def _pressed(self, event):
        self.pressed[event.char] = True

    def _released(self, event):
        self.pressed[event.char] = False
    
    def _click(self, event):
        if self.inSideMenu:
            action = self.sideMenu.updateClick((event.x, event.y))
            if action == "restart":
                self.initLevel(0)
            elif action == "menu":
                self.inLevel = False
                self.inSideMenu = False
                self.inMenu = True
                self.sounding = False
                self.vol = True
            elif action == "volToggle":
                self.vol = not self.vol
                if not self.vol:
                    self.sounding = False
        elif self.inMenu:
            action = self.Menu.updateClick((event.x, event.y))
            if action != None:
                self.inMenu = False
                self.inLevel = True
                self.sounding = False
                self.level = action
                self.initLevel()
    
    def _move(self, event):
        if self.inLevel:
            self.inSideMenu =  (p.dist((event.x, event.y), (50, 50)) <= 120)
            if self.inSideMenu:
                self.sideMenu.updateMove((event.x, event.y))
        elif self.inMenu:
          self.Menu.updateMove((event.x, event.y))
        
    def _animate(self):
        self.canvas.delete(ALL)
        self.sounds()
        self.onStep()
        self.onDraw()
        if not self.quit:
            self.root.after(1000/self.fps, self._animate)

    #sounds====================================================================
    def sounds(self):
        if not self.vol:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            return None
        if self.sounding:
            return None
        elif self.inMenu:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            winsound.PlaySound("aud" + os.sep + "menu.wav",
                               winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            self.sounding = True
        elif self.inLevel:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            winsound.PlaySound("aud" + os.sep + "menu.wav",
                               winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            self.sounding = True

    #onInit====================================================================
    def initLevel(self, default=1):
        if default > 0:
            self.Loading.draw(self.canvas, (0, 0))
            self.canvas.update_idletasks()
            L = len(self.Levels)
            self.loadLevel(self.Levels[self.level % L]())
        else:
            self.reloadLevel()
            self.inLevel = True
        subprocess.Popen(["python", self.path + os.sep + "aud" + os.sep + "start.py"])

    def loadLevel(self, levelData):
        self.wp = levelData["wp"]
        self.globalWidth = levelData["width"]
        self.globalHeight = levelData["height"]
        self.bg = menu.BG(levelData["bg"])
        self.wormhole = levelData["wormhole"]
        self.guards = levelData["guards"]
        self.objBack = levelData["backObj"]
        self.objFront = levelData["frontObj"] + [self.wormhole] + self.guards
        self.objList = self.objBack + self.objFront
        self.step = 0
        self.cam = c.Camera((self.width, self.height), (self.globalWidth, self.globalHeight), (self.wp.x, self.wp.y))
        self.restart = [copy.copy(levelData["wp"])] + copy.copy([copy.copy(guard).P for guard in self.objFront if isinstance(guard, Guard)])
        self.inLevel = True

    def reloadLevel(self):
        restart = copy.copy(self.restart)
        self.wp = copy.copy(restart[0])
        i = 1
        for obj in self.objList:
            if isinstance(obj, Guard):
                obj.P = restart[i]
                obj.index = 0
                obj.isActive = True
                obj.img = obj.imgActive
                i += 1
            elif isinstance(obj, Vial):
                obj.lit = True
                obj.img = obj.imgF
        self.cam = c.Camera((self.width, self.height),
                            (self.globalWidth, self.globalHeight),
                            (self.wp.x, self.wp.y))
    
    #onStep====================================================================
    def onStep(self):
        if self.inSideMenu:
            return None
        elif self.inLevel:
            self.onKey()
            self.gameStep()
        elif self.inMovie:
            self.inMovie = False
            self.inMenu = True

    def gameStep(self):
        self.wp.update()
        for guard in self.guards:
            guard.update()
        if self.wormhole.complete(self.wp) or self.wp.health == 0:
            if self.wp.health: #go to new level, not restarting
                if self.level != self.maxLevel:
                    self.level += 1
                else:
                    self.inLevel = False
                    self.inMovie = True
                    return None
            time.sleep(2)
            self.inLevel = False
            self.initLevel(self.wp.health)
            return None
        temp = False
        for obj in self.objList:
            temp |= obj.collision(self.wp)
        if not temp:
            self.wp.collision = False
        self.cam.follow(self.wp)

    def onKey(self):
        if self.pressed["a"] and self.wp.isParticle:
            self.wp.move_left()
        if self.pressed["d"] and self.wp.isParticle:
            self.wp.move_right()
        if self.pressed["w"]:
            if self.wp.isParticle:
                self.wp.move_up()
            else:
                self.wp.transform()
        if self.pressed["r"]:
            self.initLevel(0)
    
    #onDraw====================================================================
    def onDraw(self):
        if self.inLevel:
            self.cam.draw(self.canvas,
                          [self.bg] + self.objBack + [self.wp] + self.objFront)
            if self.inSideMenu:
                self.sideMenu.draw(self.canvas)
        elif self.inMenu:
            self.Menu.draw(self.canvas)
        elif self.inMovie:
            img = ImageTk.PhotoImage(Image.open("img" + os.sep + "endgame.png"))
            self.canvas.create_image(0, 0, anchor=NW, image=img)
            self.canvas.update_idletasks()
            time.sleep(10)

    #run=======================================================================
    def run(self):
        self._animate()
        self.root.mainloop()

Duality(width=800, height=600, fps=50).run()
winsound.PlaySound(None, winsound.SND_FILENAME)