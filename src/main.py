import sys, pygame
import keyinput, treemanager, draw, playercontrol
import gameglobals, cameracontrols, gamecontrol
import menucontrol, menudraw
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
def initialiseGame(args, mode):
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
		gamecontrol.initialiseStandard(args[0], args[1])
	elif mode == 1: # endless
		gamecontrol.initialiseEndless(args[0], args[1])
	elif mode == 2: # puzzle
		pass
	elif mode == 3: # tutorial
		gamecontrol.initialiseTutorial()
		draw.initialiseTutorial()

def uninitialiseGame():
	draw.uninitialise()

def uninitialiseMenu():
	menudraw.uninitialise()	

def gameUpdate():
	global frame
	treemanager.update()
	cameracontrols.cameraUpdate()
	gamecontrol.update(frame)
	frame += 1

	if gameglobals.gameStats.gameExited:
		initialiseMenu()

def initialiseMenu():
	uninitialiseGame()

	global inMenu
	inMenu = True
	menudraw.initialise()
	menucontrol.initialise(lambda rate, size: initialiseGame([rate, size], 0),
							lambda rate, hp: initialiseGame([rate, hp], 1),
							None,
							lambda : initialiseGame(None, 3))

def menuUpdate():
	menucontrol.update()

		
def main():
	global inMenu
	initialiseMenu()
	while 1:
		eventRead()
		if inMenu: menuUpdate()
		else: gameUpdate()

		if inMenu: menudraw.drawMenuFrame()
		else: draw.drawGameFrame()
		pygame.time.delay(20)
	
main()