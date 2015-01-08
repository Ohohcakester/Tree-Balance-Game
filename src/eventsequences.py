import gameglobals, gameeventsequence, gamecontrol

def initialise(stage):
	#-1 = tutorial.
	#1... = stage i (puzzle mode)
	if stage == -1:
		gameglobals.eventSequence = TutorialSequence()


class TutorialSequence(gameeventsequence.EventSequence):

	def start(self):
		gameglobals.gameStats = gamecontrol.GameStats(50, 20)
		gameglobals.controller = None
		gameglobals.opQueue = gamecontrol.OperationQueue()
		gameglobals.tree.add(3)
		gameglobals.tree.add(2)
		gameglobals.tree.add(4)
		gameglobals.tree.add(1)
		gameglobals.player.goLeft()
		gameglobals.player.goLeft()
		gameglobals.player.goLeft()

		self.pauseQueue()
		gameglobals.opQueue.enqueue(3, False)
		gameglobals.opQueue.enqueue(2, False)
		gameglobals.opQueue.enqueue(4, False)
		gameglobals.opQueue.enqueue(1, False)
		gameglobals.opQueue.enqueue(5, True)
		gameglobals.opQueue.enqueue(1, True)
		gameglobals.opQueue.enqueue(2, True)

		self.setPromptText('Unbalance the tree to continue')

	def defineEvents(self):
		self.addEvent(0, lambda : self.hpDrained(), lambda : self.t1_complete())

	def setPromptText(self, message):
		gameglobals.gameStats.setPromptText(message)

	def clearPromptText(self):
		gameglobals.gameStats.clearPromptText()

	def pauseQueue(self):
		gameglobals.gameStats.pauseCooldown()

	def resumeQueue(self):
		gameglobals.gameStats.resumeCooldown()

	def setTimer(self, frames):
		self.timerTime = frames

	def timerTick(self):
		if self.timerTime <= 0:
			return True
		else:
			self.timerTime -= 1

	def hpDrained(self):
		return gameglobals.gameStats.hp < 10

	def fullHp(self):
		return gameglobals.gameStats.hp >= gameglobals.gameStats.maxHp

	def drainHp(self):
		gameglobals.gameStats.hp = 0

	def t1_complete(self):
		self.clearPromptText()
		self.resumeQueue()
		gameglobals.gameStats.accelerateSpawn(1.2)
		self.clearEvents()
		self.addEvent(0, lambda : self.queueRemaining(3),
						lambda : gameglobals.gameStats.accelerateSpawn(1))
		self.addEvent(0, lambda : self.queueRemaining(0), lambda : self.t2_start())

	def queueRemaining(self, atMost):
		return gameglobals.opQueue.size() <= atMost

	def t2_start(self):
		self.setPromptText('Balance the tree to continue. Hint: you need two rotations.')
		self.seqNo = 1
		self.drainHp()
		gameglobals.player.goUp()
		gameglobals.player.goUp()
		gameglobals.player.goUp()
		self.pauseQueue()
		gameglobals.opQueue.enqueue(3, True)
		gameglobals.opQueue.enqueue(4, True)
		self.clearEvents()
		self.addEvent(1, lambda : self.fullHp(), lambda : self.t2a_complete())

	def t2a_complete(self):
		self.clearPromptText()
		self.resumeQueue()
		self.clearEvents()
		self.addEvent(1, lambda : self.queueRemaining(0), lambda : self.t2b_start())

	def t2b_start(self):
		self.setPromptText('Balance the tree to continue')
		self.clearEvents()
		self.setTimer(30)
		self.addEvent(1, lambda : self.timerTick() and self.fullHp(),
						lambda : self.t2b_complete())


	def t2b_complete(self):
		self.clearPromptText()
		if gameglobals.tree.root.data != 2:
			gameglobals.opQueue.enqueue(1, False)
			gameglobals.opQueue.enqueue(2, False)
			gameglobals.opQueue.enqueue(1, True)
			gameglobals.opQueue.enqueue(2, True)
			self.clearEvents()
			self.addEvent(1, lambda : self.queueRemaining(2),
							lambda : self.t2c_start())
		else:
			self.t2_complete()

	def t2c_start(self):
		self.setPromptText('Balance the tree to continue')
		self.drainHp()
		self.pauseQueue()
		self.clearEvents()
		self.addEvent(1, lambda : self.fullHp(),
					 	lambda : self.t2_complete())

	def t2_complete(self):
		self.clearPromptText()
		self.seqNo = 2
		self.resumeQueue()
		gameglobals.opQueue.enqueue(7, True)
		gameglobals.opQueue.enqueue(6, True)
		gameglobals.opQueue.enqueue(8, True)
		self.clearEvents()
		self.addEvent(2, lambda : self.queueRemaining(1), 
						lambda: self.t3_start())

	def t3_start(self):
		self.setPromptText('Balance the tree to continue')
		self.pauseQueue()
		self.drainHp()
		self.clearEvents()
		self.addEvent(2, lambda : self.fullHp(), lambda : self.t3_complete())

	def t3_complete(self):
		self.setPromptText('Congratulations! You have completed the tutorial!')
		self.resumeQueue()
