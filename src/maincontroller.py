import gameglobals, eventsequences, gamecontrol

controllerUpdate = None
updateScore = None

def loseGame():
	updateScore(False)
	gameglobals.gameStats.gameOver = True
	gameglobals.gameStats.victory = False

def winGame():
	updateScore(True)
	gameglobals.gameStats.gameOver = True
	gameglobals.gameStats.victory = True

def updateScoreStandard(levelIndex, victory):
	if victory:
		result = 10000
	else:
		result = gameglobals.gameStats.getFourDigitPercentage()
	gameglobals.saveData.tryUpdateStandard(levelIndex, result)

def updateScoreEndless(levelIndex, victory):
	gameglobals.saveData.tryUpdateEndless(levelIndex,
		gameglobals.gameStats.numOperations())

def updateScorePuzzle(levelIndex, victory):
	if not victory: return
	gameglobals.saveData.tryUpdatePuzzle(levelIndex,
		gameglobals.gameStats.numRotations())


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


def initialiseStandard(levelIndex, rate, size, hp):
	global controllerUpdate, updateScore
	gameglobals.gameStats = gamecontrol.GameStats(hp, rate)
	gameglobals.controller = gamecontrol.OperationController(size)
	gameglobals.opQueue = gameglobals.controller.queue
	controllerUpdate = lambda : update_standard()
	updateScore = (lambda levelIndex : \
		lambda victory : updateScoreStandard(levelIndex, victory))(levelIndex)


def initialiseEndless(levelIndex, rate, hp):
	global controllerUpdate, updateScore
	gameglobals.gameStats = gamecontrol.GameStats(hp, rate)
	gameglobals.controller = gamecontrol.OperationController(20)
	gameglobals.opQueue = gameglobals.controller.queue
	controllerUpdate = lambda : update_endless()
	updateScore = (lambda levelIndex : \
		lambda victory : updateScoreEndless(levelIndex, victory))(levelIndex)


def initialiseTutorial():
	global controllerUpdate, updateScore
	eventsequences.initialise(-1)
	controllerUpdate = lambda : update_tutorial()
	updateScore = lambda : None


def initialisePuzzle(levelIndex, stage):
	global controllerUpdate, updateScore
	eventsequences.initialise(stage)
	controllerUpdate = lambda : update_puzzle()
	updateScore = (lambda levelIndex : \
		lambda victory : updateScorePuzzle(levelIndex, victory))(levelIndex)

