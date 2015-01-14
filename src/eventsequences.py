import gameglobals, gameeventsequence, gamecontrol
from queue import Queue

def initialise(stage):
	#-1 = tutorial.
	#1... = stage i (puzzle mode)
	if stage == -1:
		gameglobals.eventSequence = TutorialSequence()
	elif stage >= 1:
		gameglobals.eventSequence = PuzzleSequence(stage)



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

	def winConditionImmediate(self):
		currentNode = gameglobals.player.currentNode
		return currentNode != None and currentNode.data == 8


class PuzzleSequence(gameeventsequence.EventSequence):

	def __init__(self, stage):
		self.stage = stage
		gameeventsequence.EventSequence.__init__(self)


	def start(self):
		gameglobals.gameStats = gamecontrol.GameStats(50, 20)
		gameglobals.controller = None
		gameglobals.opQueue = gamecontrol.OperationQueue()
		self.pauseQueue()
		self.setupStage(self.stage)

	def setup(self, stageDetails):
		for i in stageDetails.treeList:
			gameglobals.tree.add(i)
		self.winCondition = lambda tree : stageDetails.winCondition(tree)
		self.setPromptText(stageDetails.objective)

	def setupStage(self, stage):
		if stage == 1: self.setup(Stage1())
		elif stage == 2: self.setup(Stage2())
		elif stage == 3: self.setup(Stage3())
		elif stage == 4: self.setup(Stage4())
		elif stage == 5: self.setup(Stage5())
		elif stage == 6: self.setup(Stage6())
		elif stage == 7: self.setup(Stage7())
		elif stage == 8: self.setup(Stage8())
		elif stage == 9: self.setup(Stage9())
		elif stage == 10: self.setup(Stage10())
		elif stage == 11: self.setup(Stage11())
		elif stage == 12: self.setup(Stage12())
		elif stage == 13: self.setup(Stage13())
		elif stage == 14: self.setup(Stage14())
		elif stage == 15: self.setup(Stage15())
		elif stage == 16: self.setup(Stage16())
		elif stage == 17: self.setup(Stage17())
		elif stage == 18: self.setup(Stage18())
		elif stage == 19: self.setup(Stage19())
		elif stage == 20: self.setup(Stage20())
		elif stage == 21: self.setup(Stage21())
		elif stage == 22: self.setup(Stage22())
		elif stage == 23: self.setup(Stage23())
		elif stage == 24: self.setup(Stage24())
		elif stage == 25: self.setup(Stage25())
		elif stage == 26: self.setup(Stage26())
		elif stage == 27: self.setup(Stage27())
		elif stage == 28: self.setup(Stage28())
		elif stage == 29: self.setup(Stage29())
		elif stage == 30: self.setup(Stage30())


class Stage1:
	def __init__(self):
		self.treeList = [7,6,5,4,3,2,1]
		self.objective = 'Make the binary tree perfectly balanced! (full binary tree)'

		#optimal = 5?
		self.gold = 5
		self.par = 8

	def winCondition(self, tree):
		return tree.height == 3


class Stage2:
	def __init__(self):
		self.treeList = [2,1,6,5,7,3,4]
		self.objective = 'Make 4 the root! (the top of the tree)'

		#optimal = 4
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.root != None and tree.root.data == 4


class Stage3:
	def __init__(self):
		self.treeList = [3,2,7,1,5,4,6]
		self.objective = 'Make the binary tree perfectly balanced! (full binary tree)'

		#optimal = 6?
		self.gold = 6
		self.par = 10

	def winCondition(self, tree):
		return tree.height == 3


class Stage4:
	def __init__(self):
		self.treeList = [3,2,7,1,5,4,6]
		self.objective = 'Maximise the tree height'

		#optimal = ?
		self.gold = 3
		self.par = 5

	def winCondition(self, tree):
		return tree.height == 7


class Stage5:
	def __init__(self):
		self.treeList = [4,2,6,1,3,5,7]
		self.objective = 'Make 5 the right child of 3'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		node3 = tree.treeNodes[tree.indexOf(3)]
		nodeR = node3.right
		return nodeR != None and nodeR.data == 5


class Stage6:
	def __init__(self):
		self.treeList = [4,2,1,3]
		self.objective = 'Mirror the tree!'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.levelOrderMatches([1,3,2,4])


class Stage7:
	def __init__(self):
		self.treeList = [8,7,9,6,10,3,13,2,4,12,14,1,5,11,15]
		self.objective = 'Give all nodes a non-negative balance.'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance < 0:
				return False
		return True


class Stage8:
	def __init__(self):
		self.treeList = [8,7,9,6,10,3,13,2,4,12,14,1,5,11,15]
		self.objective = 'Make the binary tree perfectly balanced! (full binary tree)'
		
		#optimal = ?
		self.gold = 8
		self.par = 10

	def winCondition(self, tree):
		return tree.height == 4


class Stage9:
	def __init__(self):
		self.treeList = [1,9,2,8,3,7,4,6,5]
		self.objective = 'Mirror the tree!'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.levelOrderMatches([9,1,8,2,7,3,6,4,5])


class Stage10:
	def __init__(self):
		self.treeList = [4,2,6,1,3,5]
		self.objective = 'One node with balance 3, one node with balance -3.'
		
		#optimal = ?
		self.gold = 4
		self.par = 8

	def winCondition(self, tree):
		pos3 = False
		neg3 = False
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance == 3:
				pos3 = True
			elif tree.treeNodes[i].balance == -3:
				neg3 = True
			if pos3 and neg3:
				return True
		return False


class Stage11:
	def __init__(self):
		self.treeList = [13,3,15,1,4,14,2,10,9,12,7,11,5,8,6]
		self.objective = 'Maximise the height of the tree!'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		return tree.height == 15


class Stage12:
	def __init__(self):
		self.treeList = [8,4,11,2,6,9,13,1,3,5,7,10,12,14]
		self.objective = 'Mirror the tree!'
		
		#optimal = ?
		self.gold = 6
		self.par = 8

	def winCondition(self, tree):
		return tree.levelOrderMatches([7,4,11,2,6,9,13,1,3,5,8,10,12,14])


class Stage13:
	def __init__(self):
		self.treeList = [8,1,9,2,4,3,5,6,7]
		self.objective = 'Make the tree symmetrical!'
		
		#optimal = ?
		self.gold = 4
		self.par = 5

	def winCondition(self, tree):
		leftQueue = Queue(maxsize=9)
		rightQueue = Queue(maxsize=9)
		if tree.root.left == None or tree.root.right == None:
			return False #assume size >= 3
		leftQueue.put(tree.root.left, False)
		rightQueue.put(tree.root.right, False)
		while not leftQueue.empty():
			left = leftQueue.get()
			right = rightQueue.get()
			if (left.left == None) != (right.right == None):
				return False
			if left.left != None:
				leftQueue.put(left.left, False)
				rightQueue.put(right.right, False)
			if (left.right == None) != (right.left == None):
				return False
			if left.right != None:
				leftQueue.put(left.right, False)
				rightQueue.put(right.left, False)
		return True


class Stage14:
	def __init__(self):
		self.treeList = [3,1,6,2,4,8,5,7]
		self.objective = 'Numbers <5 have positive balance, ' + \
						'Numbers >5 have negative balance.'
		
		#optimal = ?
		self.gold = 4
		self.par = 5

	def winCondition(self, tree):
		nodes = tree.treeNodes
		for i in  range(0,len(nodes)):
			if nodes[i].data < 5:
				if nodes[i].balance <= 0:
					return False
			elif nodes[i].data > 5:
				if nodes[i].balance >= 0:
					return False
		return True
		

class Stage15:
	def __init__(self):
		self.treeList = [4,12,2,9,15,8,18,13,11,7,3,1,10,14,5,16,17,6]
		self.objective = 'All nodes with balance 0 or -1'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		balances = [0,-1]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance not in balances:
				return False
		return True


class Stage16: #HARD!
	def __init__(self):
		self.treeList = [7,2,9,1,4,8,11,3,6,10,13,5,12,15,14]
		self.objective = 'Mirror the tree!'
		
		#optimal = ?
		self.gold = 13
		self.par = 18

	def winCondition(self, tree):
		return tree.levelOrderMatches([9,7,14,5,8,12,15,3,6,10,13,1,4,11,2])
		

class Stage17:
	def __init__(self):
		self.treeList = [4,2,9,1,3,5,11,7,10,12,6,8]
		self.objective = 'Maximise the height (5) while keeping the tree balanced!' +\
						' (balance between -1 and 1)'
		
		#optimal = ?
		self.gold = 6
		self.par = 8

	def winCondition(self, tree):
		if tree.height != 5:
			return False
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance > 1 or tree.treeNodes[i].balance < -1:
				return False
		return True


class Stage18:
	def __init__(self):
		self.treeList = [5,1,9,4,6,10,2,7,11,3,8]
		self.objective = 'Mirror the tree!'
		
		#optimal = ?
		self.gold = 15 #(probably improvable?)
		self.par = 19

	def winCondition(self, tree):
		return tree.levelOrderMatches([7,3,11,2,6,8,1,5,10,4,9])


class Stage19:
	def __init__(self):
		self.treeList = [5,3,8,2,4,6,9,1,7]
		self.objective = 'Only multiples of 4 have non-zero balance!'
		
		#optimal = ?
		self.gold = 5 #(probably improvable?)
		self.par = 18

	def winCondition(self, tree):
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%4 == 0:
				if tree.treeNodes[i].balance == 0:
					return False
			else:
				if tree.treeNodes[i].balance != 0:
					return False
		return True


class Stage20: #HARD!
	def __init__(self):
		self.treeList = [6,2,11,1,4,8,12,3,5,7,9,10]
		self.objective = 'All even nodes below the odd nodes!'
		
		#optimal = ?
		self.gold = 11 #(probably improvable?)
		self.par = 18

	def winCondition(self, tree):
		heights = tree.generateHeightArray()
		maxOdd = 0
		minEven = 10000
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%2 == 1: #odd
				maxOdd = max(maxOdd, heights[i])
			else: #even
				minEven = min(minEven, heights[i])
		return maxOdd < minEven



class Stage21:
	def __init__(self):
		self.treeList = [2,1,10,6,11,4,8,3,5,7,9]
		self.objective = 'Exactly 3 nodes with balance 4.'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		count = 0
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance == 4:
				count += 1
		return count == 3


class Stage22:
	def __init__(self):
		self.treeList = [6,1,8,4,5,3,2,7]
		self.objective = 'Only primes have non-zero balance!'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		primes = [2,3,5,7]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data in primes:
				if tree.treeNodes[i].balance == 0:
					return False
			else:
				if tree.treeNodes[i].balance != 0:
					return False
		return True


class Stage23:
	def __init__(self):
		self.treeList = [3,1,8,2,6,9,5,7,4]
		self.objective = 'Even numbers have even balance, odd numbers have odd balance!'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%2 == 0:
				if tree.treeNodes[i].balance%2 == 1:
					return False
			else:
				if tree.treeNodes[i].balance%2 == 0:
					return False
		return True


class Stage24:
	def __init__(self):
		self.treeList = [8,7,3,4,9,11,1,10,2,6,5]
		self.objective = 'Exactly 5 nodes with balance 1 or -1'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		count = 0
		balances = [1,-1]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances:
				count += 1
		return count == 5


class Stage25:
	def __init__(self):
		self.treeList = [5,4,7,6,9,8,11,10,12]
		self.objective = 'Primes are below non-primes'
		
		#optimal = ?
		self.gold = 8
		self.par = 11

	def winCondition(self, tree):
		primes = [5,7,11]
		heights = tree.generateHeightArray()
		maxNonPrime = 0
		minPrime = 10000
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data in primes:
				minPrime = min(minPrime, heights[i])
			else:
				maxNonPrime = max(maxNonPrime, heights[i])
		return maxNonPrime < minPrime


class Stage26:
	def __init__(self):
		self.treeList = [5,7,15,9,2,1,4,11,10,18,12,14,16,8,17,3,13,6]
		self.objective = '5 nodes with balance +/- 3'
		
		#optimal = ?
		self.gold = 5
		self.par = 9

	def winCondition(self, tree):
		count = 0
		balances = [-3,3]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances:
				count += 1
		return count == 5


class Stage27:
	def __init__(self):
		self.treeList = [6,2,8,1,5,7,10,4,9,11,3]
		self.objective = 'Make a tree, then mirror it with one rotation.'
		
		#optimal = ?
		self.gold = 5
		self.par = 7

		self.previousLeft = [-1]*len(self.treeList)
		self.previousRight = [-1]*len(self.treeList)

	def snapshotTreeReturnFalse(self, tree):
		free = 1
		nodes = [-1]*len(self.treeList)
		nodes[0] = tree.root
		for i in range(0,len(self.treeList)):
			if nodes[i].left == None:
				self.previousLeft[i] = -1
			else:
				nodes[free] = nodes[i].left
				self.previousLeft[i] = free
				free += 1

			if nodes[i].right == None:
				self.previousRight[i] = -1
			else:
				nodes[free] = nodes[i].right
				self.previousRight[i] = free
				free += 1
		return False

	def winCondition(self, tree):
		#ASSUMPTION: THIS IS CALLED ONCE PER ROTATION
		#compare with snapshot
		free = 1
		nodes = [-1]*len(self.treeList)
		nodes[0] = tree.root
		for i in range(0,len(self.treeList)):
			if nodes[i].right == None:
				if self.previousLeft[i] != -1:
					return self.snapshotTreeReturnFalse(tree)
			else:
				nodes[free] = nodes[i].right
				if self.previousLeft[i] != free:
					return self.snapshotTreeReturnFalse(tree)
				free += 1

			if nodes[i].left == None:
				if self.previousRight[i] != -1:
					return self.snapshotTreeReturnFalse(tree)
			else:
				nodes[free] = nodes[i].left
				if self.previousRight[i] != free:
					return self.snapshotTreeReturnFalse(tree)
				free += 1
		return True


class Stage28:
	def __init__(self):
		self.treeList = [5,7,15,9,18,1,4,20,11,2,10,19,12,14,16,8,17,3,13,6]
		self.objective = 'No nodes with balance 1, -1, 2 or -2, or above 5/below -5'
		
		#optimal = ?
		self.gold = 17
		self.par = 28

	def winCondition(self, tree):
		balances = [1,-1,2,-2]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances or \
					tree.treeNodes[i].balance > 5 or \
					tree.treeNodes[i].balance < -5:
				return False
		return True


class Stage29:
	def __init__(self):
		self.treeList = [5,21,7,15,9,11,2,20,24,10,19,12,27,14,25,8,18,16,26,1,4,22,23,17,3,13,6]
		self.objective = 'Maximise height (8) while keeping balances between -2 and 2.'
		
		#optimal = ?
		self.gold = 14
		self.par = 22

	def winCondition(self, tree):
		if tree.height < 8:
			return False
		balances = [0,1,-1,2,-2]
		for i in range(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance not in balances:
				return False
		return True


		#self.treeList = [1,2,3,7,6,5,4,3]
		#self.treeList = [8,4,2,6,1,3,5,7]
		#self.treeList = [7,1,6,2,5,3,4]
		#self.treeList = [8,4,11,2,6,9,13,1,3,5,7,10,12,14]
		#self.treeList = [3,1,4,2,5,6,7]
		#self.treeList = [7,2,9,1,4,8,11,3,6,10,13,5,12]