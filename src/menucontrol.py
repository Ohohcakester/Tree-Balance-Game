import gameglobals, puzzlelevels
from enum import IntEnum

class MenuScreen(IntEnum):
	main = 0
	mode_standard = 1
	mode_endless = 2
	mode_puzzle = 3

class MenuVars:
	#each entry refers to the corresponding MenuScreen above.
	numOptions = [4, 4, 3, puzzlelevels.numPuzzles]
	tileColumns = 6;

	def __init__(self):
		self.currentOptions = [0]*len(self.numOptions)
		self.buttonOperations = self.defineButtonOperations()
		self.descriptionTexts = self.defineDescriptionTexts()
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

		operations[1][0] = lambda : start_standard(0, 130, 20, 2200)
		operations[1][1] = lambda : start_standard(1, 90, 30, 1600)
		operations[1][2] = lambda : start_standard(2, 70, 40, 1000)
		operations[1][3] = lambda : start_standard(3, 60, 80, 1000)

		operations[2][0] = lambda : start_endless(0, 60, 6000)
		operations[2][1] = lambda : start_endless(1, 40, 4000) 
		operations[2][2] = lambda : start_endless(2, 20, 3000)

		for i in range(0,self.numOptions[3]):
			operations[3][i] = (lambda target : lambda : start_puzzle(target))(i+1)

		return operations

	def defineDescriptionTexts(self):
		descriptions = self.generateEmptyArray()

		descriptions[0][0] = "Standard Mode: Survive until the end of the queue!"
		descriptions[0][1] = "Endless Mode: Survive as many operations as you can!"
		descriptions[0][2] = "Puzzle Mode: Take your time and solve increasingly difficult puzzles!"
		descriptions[0][3] = "Learn the rules of Tree Balance"

		descriptions[1][0] = "Select a difficulty"
		descriptions[1][1] = "Select a difficulty"
		descriptions[1][2] = "Select a difficulty"
		descriptions[1][3] = "Select a difficulty"

		descriptions[2][0] = "Survive as long as you can."
		descriptions[2][1] = "The binary tree changes very quickly. Can you keep up with the pace?"
		descriptions[2][2] = "The binary tree changes at a rate that is near impossible to keep up with."

		for i in range(0,self.numOptions[3]):
			descriptions[3][i] = puzzlelevels.getStage(i+1).objective

		return descriptions



	def defineBackOperations(self):
		operations = [MenuScreen.main]*len(self.numOptions)

		return operations

	def currentOption(self):
		return self.currentOptions[self.currentMenu]

	def getDescriptionText(self):
		return self.descriptionTexts[self.currentMenu][self.currentOption()]

	def getScoreValue(self):
		if self.currentMenu == MenuScreen.mode_standard:
			return gameglobals.saveData.standardScores[self.currentOption()]
		elif self.currentMenu == MenuScreen.mode_endless:
			return gameglobals.saveData.endlessScores[self.currentOption()]
		elif self.currentMenu == MenuScreen.mode_puzzle:
			return gameglobals.saveData.puzzleScores[self.currentOption()]
		else:
			return None

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

	if gameglobals.menu == None:
		gameglobals.menu = MenuVars()



def update():
	pass