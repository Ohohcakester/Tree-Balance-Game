import pygame, gameglobals

class KeyInput:
	left = 0
	right = 0
	up = 0
	a = 0
	d = 0

keys = KeyInput()


def keyPress(key):
	if (key == pygame.K_LEFT):
		gameglobals.player.goLeft()
	elif (key == pygame.K_RIGHT):
		gameglobals.player.goRight()
	elif (key == pygame.K_UP):
		gameglobals.player.goUp()
	elif (key == pygame.K_a):
		gameglobals.player.rotateLeft()
	elif (key == pygame.K_d):
		gameglobals.player.rotateRight()
	elif (key == pygame.K_ESCAPE):
		gameglobals.gameStats.exitGame()


def keyPressMenu(key):
	if (key == pygame.K_UP):
		gameglobals.menu.goUp()
	elif (key == pygame.K_DOWN):
		gameglobals.menu.goDown()
	elif (key == pygame.K_RETURN or key == pygame.K_SPACE):
		gameglobals.menu.enter()
	elif (key == pygame.K_ESCAPE):
		gameglobals.menu.goBack()

	
"""
	if (key == pygame.K_LEFT):
		keys.left = 1
	elif (key == pygame.K_RIGHT):
		keys.right = 1
	elif (key == pygame.K_UP):
		keys.up = 1
	elif (key == pygame.K_a):
		keys.a = 1
	elif (key == pygame.K_d):
		keys.d = 1

def keyRelease(key):
	if (key == pygame.K_LEFT):
		keys.left = 0
	elif (key == pygame.K_RIGHT):
		keys.right = 0
	elif (key == pygame.K_UP):
		keys.up = 0
	elif (key == pygame.K_a):
		keys.a = 0
	elif (key == pygame.K_d):
		keys.d = 0
"""