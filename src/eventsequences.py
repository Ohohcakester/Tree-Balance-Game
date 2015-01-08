import gameglobals, gameeventsequence, gamecontrol

def initialise(stage):
	#-1 = tutorial.
	#1... = stage i (puzzle mode)
	if stage == -1:
		gameglobals.eventSequence = TutorialSequence()


class TutorialSequence(gameeventsequence.EventSequence):

	def start(self):
		gameglobals.gameStats = gamecontrol.GameStats(500, 1)
		gameglobals.controller = gamecontrol.OperationController(20)
		gameglobals.tree.add(5)
		gameglobals.tree.add(3)
		gameglobals.tree.add(7)
		gameglobals.tree.add(2)
		gameglobals.tree.add(4)
		gameglobals.tree.add(6)
		gameglobals.tree.add(8)
		gameglobals.tree.add(1)
		gameglobals.player.goLeft()
		gameglobals.player.goLeft()
		gameglobals.player.goLeft()
		gameglobals.player.goLeft()

	def defineEvents(self):
		pass