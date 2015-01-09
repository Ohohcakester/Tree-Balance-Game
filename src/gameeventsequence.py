import gameglobals

class EventSequence:
	def __init__(self):
		self.seqNo = 0
		self.gameEvents = []
		self.defineEvents()
		self.start()

	def start(self):
		pass #abstract

	def defineEvents(self):
		pass #abstract

	def clearEvents(self):
		self.gameEvents = []

	def addEvent(self, seqNo, condition, action):
		self.gameEvents.append(GameEvent(seqNo, condition, action))

	def update(self):
		for gameEvent in self.gameEvents:
			gameEvent.update(self.seqNo)
		return self.checkForWin()
			
	def setPromptText(self, message):
		gameglobals.gameStats.setPromptText(message)

	def clearPromptText(self):
		gameglobals.gameStats.clearPromptText()

	def pauseQueue(self):
		gameglobals.gameStats.pauseCooldown()

	def resumeQueue(self):
		gameglobals.gameStats.resumeCooldown()

	def checkForWin(self):
		tree = gameglobals.tree
		if tree.dirty:
			if self.winCondition(tree):
				return True
			tree.resetDirtyFlag()
		return self.winConditionImmediate()

	def winCondition(self, tree):
		return False

	def winConditionImmediate(self):
		return False


class GameEvent:
	def __init__(self, seqNo, condition, action):
		self.seqNo = seqNo
		self.condition = condition
		self.action = action
		self.triggered = False

	def update(self, currentSeqNo):
		if self.triggered:
			return
		if self.seqNo != currentSeqNo:
			return
		if not self.condition():
			return
		self.triggered = True
		self.action()
