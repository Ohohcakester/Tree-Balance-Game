from __future__ import absolute_import
import sys, pygame
import keyinput, treemanager, draw, playercontrol
import gameglobals, cameracontrols, maincontroller
import menucontrol, menudraw, savedata
pygame.init()

inMenu = True
frame = None

def eventRead():
	global inMenu
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if (inMenu):
				keyinput.keyPressMenu(event.key)
			else:
				keyinput.keyPress(event.key)
		#elif event.type == pygame.KEYUP:
		#	keyinput.keyRelease(event.key)


# 0 = standard, 1 = endless, 2 = puzzle, 3 = tutorial
def initialiseGame(args, mode, levelIndex):
	uninitialiseMenu()
	
	global inMenu, frame
	inMenu = False
	frame = 0

	draw.initialise()
	gameglobals.player = playercontrol.PlayerControl() 
	treemanager.initialise()
	playercontrol.initialise()
	cameracontrols.initialise()

	if mode == 0: # standard
		maincontroller.initialiseStandard(levelIndex, args[0], args[1], args[2])
		draw.initialiseStandard()
	elif mode == 1: # endless
		maincontroller.initialiseEndless(levelIndex, args[0], args[1])
		draw.initialiseEndless()
	elif mode == 2: # puzzle
		maincontroller.initialisePuzzle(levelIndex, args[0])
		draw.initialisePuzzle()
		treemanager.initialiseTreeImage()
	elif mode == 3: # tutorial
		maincontroller.initialiseTutorial()
		draw.initialiseTutorial()


def uninitialiseGame():
	draw.uninitialise()
	gameglobals.uninitialiseGameData()

def uninitialiseMenu():
	menudraw.uninitialise()	

def gameUpdate():
	global frame
	treemanager.update()
	cameracontrols.cameraUpdate()
	maincontroller.update(frame)
	frame += 1

	if gameglobals.gameStats.gameExited:
		initialiseMenu()

def initialiseMenu():
	uninitialiseGame()

	global inMenu
	inMenu = True
	menudraw.initialise()
	menucontrol.initialise(lambda index, rate, size, hp : initialiseGame([rate, size, hp], 0, index),
							lambda index, rate, hp : initialiseGame([rate, hp], 1, index),
							lambda puzzleNo : initialiseGame([puzzleNo], 2, puzzleNo-1),
							lambda : initialiseGame(None, 3, None))

def menuUpdate():
	menucontrol.update()


def mainUpdate(willDraw):
	eventRead()
	if inMenu: menuUpdate()
	else: gameUpdate()

	if (willDraw):
		if inMenu:
			menudraw.drawMenuFrame()
		else:
			draw.drawGameFrame()


def main():
	global inMenu, timer
	savedata.startupInitialise()
	initialiseMenu()

	excessTime = 0
	lastFrameTime = 0

	while True:
		frameTime = pygame.time.get_ticks()
		excessTime += frameTime - lastFrameTime - 25
		lastFrameTime = frameTime

		if (excessTime > 50):
			mainUpdate(False)
			excessTime -= 50
		else:
			mainUpdate(True)

		pygame.time.delay(20)
	
main()