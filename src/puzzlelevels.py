from __future__ import absolute_import
from Queue import Queue

numPuzzles = 30
stages = {
	1 : lambda : Stage1(),
	2 : lambda : Stage2(),
	3 : lambda : Stage3(),
	4 : lambda : Stage4(),
	5 : lambda : Stage5(),
	6 : lambda : Stage6(),
	7 : lambda : Stage7(),
	8 : lambda : Stage8(),
	9 : lambda : Stage9(),
	10 : lambda : Stage10(),
	11 : lambda : Stage11(),
	12 : lambda : Stage12(),
	13 : lambda : Stage13(),
	14 : lambda : Stage14(),
	15 : lambda : Stage15(),
	16 : lambda : Stage16(),
	17 : lambda : Stage17(),
	18 : lambda : Stage18(),
	19 : lambda : Stage19(),
	20 : lambda : Stage20(),
	21 : lambda : Stage21(),
	22 : lambda : Stage22(),
	23 : lambda : Stage23(),
	24 : lambda : Stage24(),
	25 : lambda : Stage25(),
	26 : lambda : Stage26(),
	27 : lambda : Stage27(),
	28 : lambda : Stage28(),
	29 : lambda : Stage29(),
	30 : lambda : Stage30()
}

def getStage(stage):
	global stages
	return stages[stage]()


class Stage1(object):
	def __init__(self):
		self.treeList = [7,6,5,4,3,2,1]
		self.objective = u'Make the binary tree perfectly balanced! (full binary tree)'

		#optimal = 4?
		self.gold = 4
		self.par = 8

	def winCondition(self, tree):
		return tree.height == 3


class Stage2(object):
	def __init__(self):
		self.treeList = [2,1,6,5,7,3,4]
		self.objective = u'Make 4 the root! (the top of the tree)'

		#optimal = 4
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.root != None and tree.root.data == 4


class Stage3(object):
	def __init__(self):
		self.treeList = [3,2,7,1,5,4,6]
		self.objective = u'Make the binary tree perfectly balanced! (full binary tree)'

		#optimal = 6?
		self.gold = 6
		self.par = 10

	def winCondition(self, tree):
		return tree.height == 3


class Stage4(object):
	def __init__(self):
		self.treeList = [3,2,7,1,5,4,6]
		self.objective = u'Maximise the tree height'

		#optimal = ?
		self.gold = 3
		self.par = 5

	def winCondition(self, tree):
		return tree.height == 7


class Stage5(object):
	def __init__(self):
		self.treeList = [4,2,6,1,3,5,7]
		self.objective = u'Make 5 the right child of 3'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		node3 = tree.treeNodes[tree.indexOf(3)]
		nodeR = node3.right
		return nodeR != None and nodeR.data == 5


class Stage6(object):
	def __init__(self):
		self.treeList = [4,2,1,3]
		self.objective = u'Mirror the tree!'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.levelOrderMatches([1,3,2,4])


class Stage7(object):
	def __init__(self):
		self.treeList = [8,7,9,6,10,3,13,2,4,12,14,1,5,11,15]
		self.objective = u'Give all nodes a non-negative balance.'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance < 0:
				return False
		return True


class Stage8(object):
	def __init__(self):
		self.treeList = [8,7,9,6,10,3,13,2,4,12,14,1,5,11,15]
		self.objective = u'Make the binary tree perfectly balanced! (full binary tree)'
		
		#optimal = ?
		self.gold = 8
		self.par = 10

	def winCondition(self, tree):
		return tree.height == 4


class Stage9(object):
	def __init__(self):
		self.treeList = [1,9,2,8,3,7,4,6,5]
		self.objective = u'Mirror the tree!'
		
		#optimal = ?
		self.gold = 4
		self.par = 6

	def winCondition(self, tree):
		return tree.levelOrderMatches([9,1,8,2,7,3,6,4,5])


class Stage10(object):
	def __init__(self):
		self.treeList = [4,2,6,1,3,5]
		self.objective = u'One node with balance 3, one node with balance -3.'
		
		#optimal = ?
		self.gold = 4
		self.par = 8

	def winCondition(self, tree):
		pos3 = False
		neg3 = False
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance == 3:
				pos3 = True
			elif tree.treeNodes[i].balance == -3:
				neg3 = True
			if pos3 and neg3:
				return True
		return False


class Stage11(object):
	def __init__(self):
		self.treeList = [13,3,15,1,4,14,2,10,9,12,7,11,5,8,6]
		self.objective = u'Maximise the height of the tree!'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		return tree.height == 15


class Stage12(object):
	def __init__(self):
		self.treeList = [8,4,11,2,6,9,13,1,3,5,7,10,12,14]
		self.objective = u'Mirror the tree!'
		
		#optimal = ?
		self.gold = 6
		self.par = 8

	def winCondition(self, tree):
		return tree.levelOrderMatches([7,4,11,2,6,9,13,1,3,5,8,10,12,14])


class Stage13(object):
	def __init__(self):
		self.treeList = [8,1,9,2,4,3,5,6,7]
		self.objective = u'Make the tree symmetrical!'
		
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


class Stage14(object):
	def __init__(self):
		self.treeList = [3,1,6,2,4,8,5,7]
		self.objective = u'Numbers <5 have positive balance, ' + \
						u'Numbers >5 have negative balance.'
		
		#optimal = ?
		self.gold = 4
		self.par = 5

	def winCondition(self, tree):
		nodes = tree.treeNodes
		for i in  xrange(0,len(nodes)):
			if nodes[i].data < 5:
				if nodes[i].balance <= 0:
					return False
			elif nodes[i].data > 5:
				if nodes[i].balance >= 0:
					return False
		return True
		

class Stage15(object):
	def __init__(self):
		self.treeList = [4,12,2,9,15,8,18,13,11,7,3,1,10,14,5,16,17,6]
		self.objective = u'All nodes with balance 0 or -1'
		
		#optimal = ?
		self.gold = 10
		self.par = 13

	def winCondition(self, tree):
		balances = [0,-1]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance not in balances:
				return False
		return True


class Stage16(object): #HARD!
	def __init__(self):
		self.treeList = [7,2,9,1,4,8,11,3,6,10,13,5,12,15,14]
		self.objective = u'Mirror the tree!'
		
		#optimal = ?
		self.gold = 13
		self.par = 18

	def winCondition(self, tree):
		return tree.levelOrderMatches([9,7,14,5,8,12,15,3,6,10,13,1,4,11,2])
		

class Stage17(object):
	def __init__(self):
		self.treeList = [4,2,9,1,3,5,11,7,10,12,6,8]
		self.objective = u'Maximise the height (5) while keeping the tree balanced!' +\
						u' (balance between -1 and 1)'
		
		#optimal = ?
		self.gold = 6
		self.par = 8

	def winCondition(self, tree):
		if tree.height != 5:
			return False
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance > 1 or tree.treeNodes[i].balance < -1:
				return False
		return True


class Stage18(object):
	def __init__(self):
		self.treeList = [5,1,9,4,6,10,2,7,11,3,8]
		self.objective = u'Mirror the tree!'
		
		#optimal = ?
		self.gold = 15 #(probably improvable?)
		self.par = 19

	def winCondition(self, tree):
		return tree.levelOrderMatches([7,3,11,2,6,8,1,5,10,4,9])


class Stage19(object):
	def __init__(self):
		self.treeList = [5,3,8,2,4,6,9,1,7]
		self.objective = u'Only multiples of 4 have non-zero balance!'
		
		#optimal = ?
		self.gold = 5 #(probably improvable?)
		self.par = 18

	def winCondition(self, tree):
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%4 == 0:
				if tree.treeNodes[i].balance == 0:
					return False
			else:
				if tree.treeNodes[i].balance != 0:
					return False
		return True


class Stage20(object): #HARD!
	def __init__(self):
		self.treeList = [6,2,11,1,4,8,12,3,5,7,9,10]
		self.objective = u'All even nodes below the odd nodes!'
		
		#optimal = ?
		self.gold = 11 #(probably improvable?)
		self.par = 18

	def winCondition(self, tree):
		heights = tree.generateHeightArray()
		maxOdd = 0
		minEven = 10000
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%2 == 1: #odd
				maxOdd = max(maxOdd, heights[i])
			else: #even
				minEven = min(minEven, heights[i])
		return maxOdd < minEven



class Stage21(object):
	def __init__(self):
		self.treeList = [2,1,10,6,11,4,8,3,5,7,9]
		self.objective = u'Exactly 3 nodes with balance 4.'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		count = 0
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance == 4:
				count += 1
		return count == 3


class Stage22(object):
	def __init__(self):
		self.treeList = [6,1,8,4,5,3,2,7]
		self.objective = u'Only primes have non-zero balance!'
		
		#optimal = ?
		self.gold = 7
		self.par = 9

	def winCondition(self, tree):
		primes = [2,3,5,7]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data in primes:
				if tree.treeNodes[i].balance == 0:
					return False
			else:
				if tree.treeNodes[i].balance != 0:
					return False
		return True


class Stage23(object):
	def __init__(self):
		self.treeList = [3,1,8,2,6,9,5,7,4]
		self.objective = u'Even numbers have even balance, odd numbers have odd balance!'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data%2 == 0:
				if tree.treeNodes[i].balance%2 == 1:
					return False
			else:
				if tree.treeNodes[i].balance%2 == 0:
					return False
		return True


class Stage24(object):
	def __init__(self):
		self.treeList = [8,7,3,4,9,11,1,10,2,6,5]
		self.objective = u'Exactly 5 nodes with balance 1 or -1'
		
		#optimal = ?
		self.gold = 4
		self.par = 7

	def winCondition(self, tree):
		count = 0
		balances = [1,-1]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances:
				count += 1
		return count == 5


class Stage25(object):
	def __init__(self):
		self.treeList = [5,4,7,6,9,8,11,10,12]
		self.objective = u'Primes are below non-primes'
		
		#optimal = ?
		self.gold = 8
		self.par = 11

	def winCondition(self, tree):
		primes = [5,7,11]
		heights = tree.generateHeightArray()
		maxNonPrime = 0
		minPrime = 10000
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].data in primes:
				minPrime = min(minPrime, heights[i])
			else:
				maxNonPrime = max(maxNonPrime, heights[i])
		return maxNonPrime < minPrime


class Stage26(object):
	def __init__(self):
		self.treeList = [5,7,15,9,2,1,4,11,10,18,12,14,16,8,17,3,13,6]
		self.objective = u'5 nodes with balance +/- 3'
		
		#optimal = ?
		self.gold = 5
		self.par = 9

	def winCondition(self, tree):
		count = 0
		balances = [-3,3]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances:
				count += 1
		return count == 5


class Stage27(object):
	def __init__(self):
		self.treeList = [6,2,8,1,5,7,10,4,9,11,3]
		self.objective = u'Make a tree, then mirror it with one rotation.'
		
		#optimal = ?
		self.gold = 5
		self.par = 7

		self.previousLeft = [-1]*len(self.treeList)
		self.previousRight = [-1]*len(self.treeList)

	def snapshotTreeReturnFalse(self, tree):
		free = 1
		nodes = [-1]*len(self.treeList)
		nodes[0] = tree.root
		for i in xrange(0,len(self.treeList)):
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
		for i in xrange(0,len(self.treeList)):
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


class Stage28(object):
	def __init__(self):
		self.treeList = [5,7,15,9,18,1,4,20,11,2,10,19,12,14,16,8,17,3,13,6]
		self.objective = u'No nodes with balance 1, -1, 2 or -2, or above 5/below -5'
		
		#optimal = ?
		self.gold = 17
		self.par = 28

	def winCondition(self, tree):
		balances = [1,-1,2,-2]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance in balances or \
					tree.treeNodes[i].balance > 5 or \
					tree.treeNodes[i].balance < -5:
				return False
		return True


class Stage29(object):
	def __init__(self):
		self.treeList = [5,21,7,15,9,11,2,20,24,10,19,12,27,14,25,8,18,16,26,1,4,22,23,17,3,13,6]
		self.objective = u'Maximise height (8) while keeping balances between -2 and 2.'
		
		#optimal = ?
		self.gold = 14
		self.par = 22

	def winCondition(self, tree):
		if tree.height < 8:
			return False
		balances = [0,1,-1,2,-2]
		for i in xrange(0,len(tree.treeNodes)):
			if tree.treeNodes[i].balance not in balances:
				return False
		return True



class Stage30(object):
	def __init__(self):
		self.treeList = [1]
		self.objective = u'WIP'
		
		#optimal = ?
		self.gold = 100
		self.par = 100

	def winCondition(self, tree):
		return False

		#self.treeList = [1,2,3,7,6,5,4,3]
		#self.treeList = [8,4,2,6,1,3,5,7]
		#self.treeList = [7,1,6,2,5,3,4]
		#self.treeList = [8,4,11,2,6,9,13,1,3,5,7,10,12,14]
		#self.treeList = [3,1,4,2,5,6,7]
		#self.treeList = [7,2,9,1,4,8,11,3,6,10,13,5,12]