import gameglobals


def initialise():
	gameglobals.cameraCenter = [0,0]

def cameraUpdate():
	currentNode = gameglobals.player.currentNode
	if (currentNode == None):
		targetPosition = [0,0]
	else:
		targetPosition = currentNode.position

	cameraCenter = gameglobals.cameraCenter
	for i in range(0,2):
		diff = -targetPosition[i] - cameraCenter[i]
		diff *= 3
		diff //= 50
		cameraCenter[i] += diff