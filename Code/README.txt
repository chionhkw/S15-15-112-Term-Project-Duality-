Keven Chionh
kchionh

###############################################################################
DESCRIPTION
###############################################################################

DUALITY (produced by Keven Chionh)
Strategy / Fantasy / Platform game

DUALITY is a platform game in which you take on the role of a red waveparticle 
whose soulmate has been abducted by the universe because you two are not a 
monochromatic couple. You exhibits both wave and particle properties of 
light. As a particle, you are like any other solid particle: affected by 
gravity and unable to pass through glass. However, upon exceeding a certain 
speed, you involuntarily transforms into a wave. No longer affected by gravity, 
you can soar to new heights. However, you can no longer control your direction. 
You are subjected to the laws of reflection and refraction. The only way to 
regain control is to slow down and morph back into a particle. Can you save 
your soulmate?

To find out, open Code\DUALITY.py

REQUIRES:
Python Imaging Library	(https://pypi.python.org/pypi/Pillow/)
numpy
Windows XP or better (sound not supported on other OS)

ALTERNATE WAY TO INSTALL PACKAGES:
download 'pip' (https://pypi.python.org/pypi/pip)
run Command Prompt as Administrator
save pip.exe to PATHS
type 'pip install pil' and 'pip install numpy' into command line

###############################################################################
DIRECTORY
###############################################################################
FILES
		Timesheet.xlsx

FOLDERS
Code
		DUALITY.py		Main file	(Credits: Dr Kosbie's eventBasedAnimation (cs.cmu.edu/~112); http://stackoverflow.com/questions/2138518/python-bind-allow-multiple-keys-to-be-pressed-simultaniously)
		physics.py		Game physics	(Credits: #http://en.wikipedia.org/wiki/Snell's_law#Vector_form)
		waveparticle.py		Object classes
		camera.py		Camera class
		levels.py		Level data
		menu.py			Menu classes
		project-video.txt	Link to Project Video
		README.txt		this

	img
		...			Many images
		credits.txt		Image credits

	aud	...			Many .wav files and associated .py files
		credits.txt		Audio credits
		

outdated	(obsolete) previous submissions
	Deliverable 1.1	(obsolete) previous submission
			camera.py
			eventBasedAnimation.py
			main.py
			physics.py
			README.txt
			updates1.txt		Copy of UPDATES section below

	Deliverable1	(obsolete) previous submission
			Project Proposal.docx

design
	project-design.txt	Project description

	... 		All older versions of DUALITY
	Movie		All files used for the video

###############################################################################
UPDATES
###############################################################################
since Deliverable 1
1. eventBasedAnimation.py, beam.py, test.py obsolete
2. collision detection split into edge detection and vertex detection
3. refraction, reflection, perPt, vangle (...) included in game physics
4. graphics included