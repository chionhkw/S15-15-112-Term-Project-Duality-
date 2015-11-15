import winsound
import os
path = os.path.dirname(__file__)
winsound.PlaySound(path + os.sep + "start.wav", winsound.SND_FILENAME)