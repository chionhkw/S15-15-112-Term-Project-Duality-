import winsound
import os
import random
path = os.path.dirname(__file__)
winsound.PlaySound(path + os.sep + "ouch%d.wav" % random.randint(1, 3), winsound.SND_FILENAME)