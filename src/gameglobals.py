from __future__ import absolute_import
import pygame

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

player = None
tree = None
cameraCenter = None

treeImage = None

gameStats = None
controller = None
opQueue = None

menu = None
saveData = None

eventSequence = None


def uninitialiseGameData():
	global player, tree, cameraCenter, gameStats
	global controller, opQueue, eventSequence
	player = None
	tree = None
	cameraCenter = None
	gameStats = None
	controller = None
	opQueue = None
	eventSequence = None
	treeImage = None

