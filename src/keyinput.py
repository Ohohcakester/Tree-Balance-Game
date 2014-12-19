import pygame, gameglobals


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
