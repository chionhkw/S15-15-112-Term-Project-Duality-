import winsound
import os
path = os.path.dirname(__file__)
winsound.PlaySound(path + os.sep + "jump.wav", winsound.SND_FILENAME)