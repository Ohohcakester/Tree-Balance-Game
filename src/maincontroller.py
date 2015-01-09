import gameglobals, eventsequences, gamecontrol

controllerUpdate = None

def loseGame():
	gameglobals.gameStats.gameOver = True
	gameglobals.gameStats.victory = False

def winGame():
	gameglobals.gameStats.gameOver = True
	gameglobals.gameStats.victory = True


def update(frame):
	if gameglobals.gameStats.gameOver: return

	global controllerUpdate
	controllerUpdate()


def update_standard():
	if hpDrain() == False:
		loseGame()
		return

	updateSpawningStandard()


def update_endless():
	if hpDrain() == False:
		loseGame()
		return

	updateSpawningEndless()


def update_tutorial():
	hpDrain()
	updateSpawningTutorial()
	if gameglobals.eventSequence.update():
		winGame()

def update_puzzle():
	#hpDrain()
	if gameglobals.eventSequence.update():
		winGame()


def updateSpawningTutorial():
	if gameglobals.gameStats.updateCooldown() == True:
		operation = gameglobals.opQueue.popNext()
		if (operation != None):
			if (operation[1] == True): # add
				gameglobals.tree.add(operation[0])
			else: # delete
				gameglobals.tree.remove(operation[0])


def updateSpawningStandard():
	if gameglobals.gameStats.updateCooldown() == True:
		operation = gameglobals.opQueue.popNext()
		gameglobals.controller.maybeChangeSpawnRate()
		if (operation != None):
			if (operation[1] == True): # add
				gameglobals.tree.add(operation[0])
			else: # delete
				gameglobals.tree.remove(operation[0])
		else:
			winGame()


def updateSpawningEndless():
	if gameglobals.gameStats.updateCooldown() == True:
		operation = gameglobals.opQueue.popNext()
		gameglobals.controller.maybeExpand()
		if (operation != None):
			if (operation[1] == True): # add
				gameglobals.tree.add(operation[0])
			else: # delete
				gameglobals.tree.remove(operation[0])


def hpDrain():
	gameStats = gameglobals.gameStats
	totalImbalance = gameglobals.tree.totalImbalance()
	gameStats.hp -= totalImbalance
	if gameStats.hp < 0:
		gameStats.hp = 0
		return False
	else:
		gameStats.hp += 0.7 #regeneration
		if (gameStats.hp > gameStats.maxHp):
			gameStats.hp = gameStats.maxHp
	return True


def initialiseStandard(rate, size, hp):
	global controllerUpdate
	gameglobals.gameStats = gamecontrol.GameStats(hp, rate)
	gameglobals.controller = gamecontrol.OperationController(size)
	gameglobals.opQueue = gameglobals.controller.queue
	controllerUpdate = lambda : update_standard()


def initialiseEndless(rate, hp):
	global controllerUpdate
	gameglobals.gameStats = gamecontrol.GameStats(hp, rate)
	gameglobals.controller = gamecontrol.OperationController(20)
	gameglobals.opQueue = gameglobals.controller.queue
	controllerUpdate = lambda : update_endless()


def initialiseTutorial():
	global controllerUpdate
	eventsequences.initialise(-1)
	controllerUpdate = lambda : update_tutorial()


def initialisePuzzle(stage):
	global controllerUpdate
	eventsequences.initialise(stage)
	controllerUpdate = lambda : update_puzzle()

