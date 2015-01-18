import gameglobals

class PlayerControl:
	
	def __init__(self):
		self.currentNode = None
		self.rotations = 0
		self.dialogOpen = False

	def selectIfUnselected(self):
		if self.currentNode != None:
			return
		self.currentNode = gameglobals.tree.root #can possibly be None

	def gameOver(self):
		return gameglobals.gameStats.gameOver


	def openDialog(self):
		self.dialogOpen = True


	def closeDialog(self):
		if self.dialogOpen:
			self.dialogOpen = False

	def goLeft(self):
		if self.dialogOpen: return

		self.selectIfUnselected()
		if (self.currentNode != None and self.currentNode.left != None):
			self.currentNode = self.currentNode.left

	def goRight(self):
		if self.dialogOpen: return
		
		self.selectIfUnselected()
		if (self.currentNode != None and self.currentNode.right != None):
			self.currentNode = self.currentNode.right

	def goUp(self):
		if self.dialogOpen: return
		
		self.selectIfUnselected()
		if (self.currentNode != None and self.currentNode.parent != None):
			self.currentNode = self.currentNode.parent

	def rotateLeft(self):
		if self.dialogOpen: return
		if (self.gameOver()): return
		if self.currentNode == None: return

		if gameglobals.tree.rotateLeft(self.currentNode):
			self.rotations += 1
			self.goUp()

	def rotateRight(self):
		if self.dialogOpen: return
		if (self.gameOver()): return
		if self.currentNode == None: return

		if gameglobals.tree.rotateRight(self.currentNode):
			self.rotations += 1
			self.goUp()

	def isSelected(self, index):
		if self.currentNode == None:
			return False
		return self.currentNode.index == index

	def relocate(self, newNode):
		self.currentNode = newNode
		

def initialise():
	gameglobals.player = PlayerControl()