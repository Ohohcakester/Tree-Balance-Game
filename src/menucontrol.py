import gameglobals
from enum import IntEnum

class MenuScreen(IntEnum):
	main = 0
	mode_standard = 1
	mode_endless = 2
	mode_puzzle = 3

class MenuVars:
	numOptions = [4, 4, 3, 30]
	tileColumns = 6;

	def __init__(self):
		self.currentOptions = [0]*len(self.numOptions)
		self.buttonOperations = self.defineButtonOperations()
		self.backOperations = self.defineBackOperations()
		self.currentMenu = MenuScreen.main
		self.optionsTextRender = self.generateEmptyArray()

	def generateEmptyArray(self):
		numMenus = len(self.numOptions)
		arr = [[]]*numMenus
		for i in range(0,numMenus):
			arr[i] = [None]*self.numOptions[i]
		return arr

	def defineButtonOperations(self):
		operations = self.generateEmptyArray()

		operations[0][0] = lambda : self.goToMenu(MenuScreen.mode_standard)
		operations[0][1] = lambda : self.goToMenu(MenuScreen.mode_endless)
		operations[0][2] = lambda : self.goToMenu(MenuScreen.mode_puzzle)
		operations[0][3] = lambda : start_tutorial()

		operations[1][0] = lambda : start_standard(130, 20, 2200)
		operations[1][1] = lambda : start_standard(90, 30, 1600)
		operations[1][2] = lambda : start_standard(70, 40, 1000)
		operations[1][3] = lambda : start_standard(60, 80, 1000)

		operations[2][0] = lambda : start_endless(60, 6000)
		operations[2][1] = lambda : start_endless(40, 4000) 
		operations[2][2] = lambda : start_endless(20, 3000)

		for i in range(0,self.numOptions[3]):
			target = i+1
			operations[3][i] = (lambda target : lambda : start_puzzle(target))(target)

		return operations

	def defineBackOperations(self):
		operations = [MenuScreen.main]*len(self.numOptions)

		return operations

	def currentOption(self):
		return self.currentOptions[self.currentMenu]

	def goToMenu(self, toMenu):
		self.currentMenu = toMenu

	def goDown(self):
		if self.currentMenu == MenuScreen.mode_puzzle:
			self.currentOptions[self.currentMenu] += self.tileColumns
			if self.currentOptions[self.currentMenu] >= self.numOptions[self.currentMenu]:
				self.currentOptions[self.currentMenu] -= self.numOptions[self.currentMenu]
		else:
			self.currentOptions[self.currentMenu] += 1
			if self.currentOptions[self.currentMenu] >= self.numOptions[self.currentMenu]:
				self.currentOptions[self.currentMenu] = 0

	def goUp(self):
		if self.currentMenu == MenuScreen.mode_puzzle:
			self.currentOptions[self.currentMenu] -= self.tileColumns
			if self.currentOptions[self.currentMenu] < 0:
				self.currentOptions[self.currentMenu] += self.numOptions[self.currentMenu]
		else:
			self.currentOptions[self.currentMenu] -= 1
			if self.currentOptions[self.currentMenu] < 0:
				self.currentOptions[self.currentMenu] = self.numOptions[self.currentMenu]-1

	def goRight(self):
		if self.currentMenu == MenuScreen.mode_puzzle:
			self.currentOptions[self.currentMenu] += 1
			if self.currentOptions[self.currentMenu] >= self.numOptions[self.currentMenu]:
				self.currentOptions[self.currentMenu] = 0

	def goLeft(self):
		if self.currentMenu == MenuScreen.mode_puzzle:
			self.currentOptions[self.currentMenu] -= 1
			if self.currentOptions[self.currentMenu] < 0:
				self.currentOptions[self.currentMenu] = self.numOptions[self.currentMenu]-1


	def enter(self):
		operation = self.buttonOperations[self.currentMenu][self.currentOptions[self.currentMenu]]
		if operation != None:
			operation()

	def goBack(self):
		self.goToMenu(self.backOperations[self.currentMenu])


start_standard = None
start_endless = None
start_puzzle = None
start_tutorial = None


def initialise(standardStartFunction, endlessStartFunction,
		puzzleStartFunction, tutorialStartFunction):
	global start_standard, start_endless, start_puzzle, start_tutorial
	start_standard = standardStartFunction
	start_endless = endlessStartFunction
	start_puzzle = puzzleStartFunction
	start_tutorial = tutorialStartFunction

	gameglobals.menu = MenuVars()



def update():
	pass