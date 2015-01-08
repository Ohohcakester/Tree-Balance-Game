import gameglobals
import random


class GameStats:

	def __init__(self, maxHp, rate):
		self.maxHp = maxHp
		self.hp = self.maxHp
		self.baseCooldown = rate
		self.cooldown = rate
		self.gameExited = False
		self.gameOver = False
		self.cooldownTimer = 30
		self.cooldownPaused = False

		self.promptText = None
		self.promptTextMessage = None

	def pauseCooldown(self):
		self.cooldownPaused = True
		self.cooldownTimer = self.cooldown

	def resumeCooldown(self):
		self.cooldownPaused = False

	def setPromptText(self, message):
		self.promptTextMessage = message
		self.promptText = None

	def clearPromptText(self):
		self.promptTextMessage = None
		self.promptText = None

	def numOperations(self):
		return gameglobals.opQueue.opCount

	def queueTotalSize(self):
		return gameglobals.opQueue.totalSize()

	def treeSize(self):
		return gameglobals.tree.size()

	def treeHeight(self):
		return gameglobals.tree.height

	def numRotations(self):
		return gameglobals.player.rotations

	def accelerateSpawn(self, multiplier):
		self.cooldown = int(self.baseCooldown / multiplier)

	def updateCooldown(self):
		if self.cooldownPaused: return False

		if self.cooldownTimer > 0:
			self.cooldownTimer -= 1
			return False
		else:
			self.cooldownTimer = self.cooldown
			return True

	def exitGame(self):
		self.gameExited = True



#Carries add / delete operations.
class OperationQueue:
	nextFewSize = 10

	def __init__(self):
		self.queue = []
		self.index = 0
		self.renderedText = []
		self.opCount = 0
		self.resetNextFewOperations()

	def enqueue(self, data, addNotDelete):
		self.queue.append([data, addNotDelete])
		if (len(self.queue) <= self.index+self.nextFewSize):
			self.resetNextFewOperations()

	def splitPoint(self):
		splitPoint = self.index + self.nextFewSize
		if splitPoint > len(self.queue):
			splitPoint = len(self.queue)
		return splitPoint

	def replaceAfterSplitPoint(self, operations):
		splitPoint = self.splitPoint()
		self.queue = self.queue[:splitPoint] + operations
		self.resetNextFewOperations()

	def getOperationsFromSplitPoint(self):
		splitPoint = self.splitPoint()
		return self.queue[splitPoint:]

	def popNext(self):
		if self.isEmpty(): return None

		operation = self.queue[self.index]
		self.index += 1
		self.resetNextFewOperations()
		self.opCount += 1
		return operation

	def isEmpty(self):
		return self.index >= len(self.queue)

	def size(self):
		size = len(self.queue) - self.index
		if size < 0:
			return 0
		else:
			return size

	def totalSize(self):
		return len(self.queue)

	def resetNextFewOperations(self):
		self.nextFewOperations = self.queue[self.index:self.index+self.nextFewSize]
		self.renderedText = None

	def onlyDeletionsLeft(self):
		for i in range(self.index,len(self.queue)):
			if self.queue[i][1] == True:
				return False
		return True
		


class OperationController:

	def __init__(self, size):
		self.queue = self.initialiseQueue(size)
		self.size = size
		self.nextUnusedNumber = size
		self.state = 0

	def maybeChangeSpawnRate(self): # used by standard mode
		if self.state == 0:
			self.state = 1
			gameglobals.gameStats.accelerateSpawn(1.4)
		elif self.state == 1:
			if self.queue.index > self.size//3:
				gameglobals.gameStats.accelerateSpawn(1)
				self.state = 2
		elif self.state == 2:
			if self.queue.onlyDeletionsLeft():
				gameglobals.gameStats.accelerateSpawn(1.6)
				self.state = 3


	def maybeExpand(self): # used by endless mode
		if self.queue.index > self.size:
			if self.state < 4:
				self.state += 1
			else:
				return
			self.expandQueue()

	def expandQueue(self):
		#Expand (size x2)
		queuedOperations = self.queue.getOperationsFromSplitPoint()
		pendingInserts = []
		pendingDeletes = []
		for operation in queuedOperations:
			if operation[1] == True: # insert
				pendingInserts.append(operation[0])
			else: # delete
				if operation[0] not in pendingInserts:
					pendingDeletes.append(operation[0])

		numNewNumbers = self.size - len(pendingInserts)
		self.size += numNewNumbers
		for i in range(0, numNewNumbers):
			pendingInserts.append(self.nextUnusedNumber)
			self.nextUnusedNumber += 1
		
		random.shuffle(pendingInserts)
		"""
		a = pendingInserts[:]
		a.sort()
		print(a)
		print("SIZE " + str(self.size))
		"""
		opSequence = self.initialiseOpSequence(len(pendingInserts))
		for i in range(0,len(pendingDeletes)):
			opSequence.append(False)
		
		operations = []
		insertedList = pendingDeletes
		index = 0
		for i in range(0,len(opSequence)):
			if opSequence[i] == True:
				#insertion
				operations.append([pendingInserts[index], True])
				insertedList.append(pendingInserts[index])
				insertedList.sort()
				index += 1
			else:
				#deletion
				rangeMax = max(len(insertedList)//3, 1)
				deleteValue = insertedList.pop(random.randrange(rangeMax))
				operations.append([deleteValue, False])

		self.queue.replaceAfterSplitPoint(operations)


	def initialiseQueue(self, size):
		queue = OperationQueue()

		opSequence = self.initialiseOpSequence(size)
		numbers = list(range(0,size))
		random.shuffle(numbers)
		insertedList = []
		index = 0
		for i in range(0,size*2):
			if (opSequence[i] == True):
				#insertion
				queue.enqueue(numbers[index], True)
				insertedList.append(numbers[index])
				index += 1
			else:
				#deletion
				deleteValue = insertedList.pop(random.randrange(len(insertedList)))
				queue.enqueue(deleteValue, False)

		return queue


	def initialiseOpSequence(self, size):
		opSequence = [] #True = add, False = delete
		insertions = 0
		deletions = 0
		for i in range(0,size*2):
			if (insertions >= size):
				opSequence.append(False)
				deletions += 1

			elif (deletions+1 < insertions/2):
				if random.randrange(3) == 0:
					opSequence.append(False)
					deletions += 1
				else:
					opSequence.append(True)
					insertions += 1
			else:
				opSequence.append(True)
				insertions += 1

		return opSequence
