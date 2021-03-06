import gameglobals, pygame, pygame.font
pygame.font.init()

class Graphics:

	def __init__(self):
		self.background = pygame.image.load("assets/bggraphic.jpg")
		bgRect = self.background.get_rect()
		self.bgHalfSize = [bgRect[2]//2, bgRect[3]//2]
		
		self.node_unselected = pygame.image.load("assets/node.png")
		self.node_selected = pygame.image.load("assets/nodeSelected.png")
		nodeRect = self.node_selected.get_rect()
		self.nodeHalfSize = nodeRect[2]//2

		self.nodeGlow = pygame.image.load("assets/nodeglow.png")
		nodeGlowRect = self.nodeGlow.get_rect()
		self.nodeGlowHalfSize = nodeGlowRect[2]//2

		self.uiBar = pygame.image.load("assets/uibar.png")

		self.addSquare = pygame.image.load("assets/addSquare.png")
		self.deleteSquare = pygame.image.load("assets/deleteSquare.png")
		squareRect = self.addSquare.get_rect()
		self.squareHalfSize = squareRect[2]//2

		self.arrowRight = pygame.image.load("assets/arrowsingle.png")
		self.arrowLeft = pygame.transform.flip(self.arrowRight, True, False)
		self.arrowDouble = pygame.image.load("assets/arrowdouble.png")
		arrowRect = self.arrowDouble.get_rect()
		self.arrowOffset = [-arrowRect[2]//2, -50]

		self.text_operations = None
		self.text_operations_value = None
		self.text_treeSize = None
		self.text_treeSize_value = None
		self.text_treeHeight = None
		self.text_treeHeight_value = None

		self.nextText = None


	def initialiseTutorialText(self):
		self.tutorialImages = [
			pygame.image.load("assets/tutorialPanel1.png"),
			pygame.image.load("assets/tutorialPanel2.png"),
			pygame.image.load("assets/tutorialPanel3.png"),
			pygame.image.load("assets/tutorialPanel4.png"),
			pygame.image.load("assets/tutorialPanel5.png"),
			pygame.image.load("assets/tutorialPanel6.png"),
			pygame.image.load("assets/tutorialPanel7.png"),
			pygame.image.load("assets/tutorialPanel8.png")]
		self.tutorialPanelHeight = self.tutorialImages[0].get_height()

		self.creditsText = None

		size = gameglobals.size
		self.text_objective = None
		self.objectiveTextPosition = [0, size[1]//2-25]
		self.promptTextPosition = [0, size[1]//2]
		self.dialogOpen = True
		self.shiftObjectiveText = lambda : self.shiftTutorialObjectiveText()


	def initialisePuzzleText(self):
		size = gameglobals.size
		self.text_par = None
		self.parTextPosition = [size[0]-80,35]
		self.rotationsTextPosition = [size[0]-180,35]
		self.TEXTCOLOUR_GOLD = 255, 240, 32
		self.TEXTCOLOUR_PAR = 100, 240, 0
		self.TEXTCOLOUR_ABOVEPAR = 255, 127, 127

		self.text_objective = None
		self.objectiveTextPosition = [0, size[1]//2-25]
		self.promptTextPosition = [0, size[1]//2]
		self.dialogOpen = True
		self.shiftObjectiveText = lambda : self.shiftPuzzleObjectiveText()


	def shiftTutorialObjectiveText(self):
		size = gameglobals.size
		self.objectiveTextPosition[1] = size[1]-225
		self.promptTextPosition[1] = size[1]-200

	def shiftPuzzleObjectiveText(self):
		self.objectiveTextPosition[1] = 45
		self.promptTextPosition[1] = 72



	def gameOver(self, isVictory):
		self.node_unselected = pygame.image.load("assets/nodeDead.png")
		self.node_selected = pygame.image.load("assets/nodeSelectedDead.png")
		if isVictory:
			self.gameOverMessage = pygame.image.load("assets/victory.png")
		else:
			self.gameOverMessage = pygame.image.load("assets/defeat.png")

		messageRect = self.gameOverMessage.get_rect()
		self.messageHalfSize = [messageRect[2]//2, messageRect[3]//2]


offset = [gameglobals.size[0]//2, gameglobals.size[1]*5//11]
balanceYOffset = 30
normalColours = False

font = pygame.font.SysFont("consolas", 20)
statsFont = pygame.font.SysFont("verdana", 16)
opsFont = pygame.font.SysFont("verdana", 18)
#font = pygame.freetype.Font("font.ttf", 12)

drawOther = lambda : None


def uninitialise():
	global graphics, drawOther
	graphics = None
	normalColours = False
	drawOther = lambda : None


def initialiseTutorial():
	global drawOther
	drawOther = lambda : drawTutorialUI()
	graphics.initialiseTutorialText()

def initialiseStandard():
	global drawOther
	drawOther = lambda : drawStandardUI()

def initialiseEndless():
	global drawOther
	drawOther = lambda : drawEndlessUI()

def initialisePuzzle():
	global drawOther, graphics
	drawOther = lambda : drawPuzzleUI()
	graphics.initialisePuzzleText()


def initialise():
	global normalColours
	global BACKGROUND_COLOUR, NODE_TEXT_COLOUR, OPS_TEXT_COLOUR
	global TEXT_COLOUR, LINE_COLOUR, HPBAR_BACK
	global HPBAR_FRONT
	global graphics

	graphics = Graphics()

	normalColours = True
	BACKGROUND_COLOUR = 0, 0, 0
	NODE_TEXT_COLOUR = 255, 64, 0
	TEXT_COLOUR = 255, 255, 255
	OPS_TEXT_COLOUR = 127, 255, 0
	LINE_COLOUR = 255, 255, 255
	HPBAR_BACK = 255, 0, 0
	HPBAR_FRONT = 0, 255, 0

def gameOverColours():
	global normalColours
	if not normalColours: return

	global LINE_COLOUR, HPBAR_BACK
	global HPBAR_FRONT
	global graphics

	graphics.gameOver(gameglobals.gameStats.victory)

	#BACKGROUND_COLOUR = 0, 0, 0
	normalColours = False
	LINE_COLOUR = 127, 127, 127
	if not gameglobals.gameStats.victory:
		HPBAR_BACK = 255, 0, 0
		HPBAR_FRONT = 255, 0, 0


def drawGameFrame():
	screen = gameglobals.screen
	if gameglobals.gameStats.gameOver:
		gameOverColours()

	screen.fill(BACKGROUND_COLOUR)

	global graphics, drawOther
	bgPosition = [gameglobals.cameraCenter[0]*2//7 + offset[0] - graphics.bgHalfSize[0],
		gameglobals.cameraCenter[1]//2 + offset[1] - graphics.bgHalfSize[1]]
	screen.blit(graphics.background, bgPosition)

	drawTree(gameglobals.tree)
	drawUIPanel()
	drawGameOverMessage()
	drawOther()

	pygame.display.flip()


def drawUIPanel():
	screen = gameglobals.screen
	global graphics
	size = gameglobals.size

	# Draw Frame
	drawPos = [0,0]
	screen.blit(graphics.uiBar, drawPos)

	# Draw Queue
	queue = gameglobals.opQueue
	operations = queue.nextFewOperations

	queueDistance = 60
	queueSize = len(operations)
	queueLeft = (size[0] - (queueSize-1)*queueDistance)//2
	posX = queueLeft
	posY = 75

	if (queue.renderedText == None):
		queue.renderedText = []
		for i in range(0, queueSize):
			text = font.render(str(operations[i][0]), True, TEXT_COLOUR)
			queue.renderedText.append(text)

	for i in range (0,queueSize):
		text = queue.renderedText[i]
		if (operations[i][1] == True): # add
			image = graphics.addSquare
		else: # delete
			image = graphics.deleteSquare
		drawPos[0] = posX-graphics.squareHalfSize
		drawPos[1] = posY-graphics.squareHalfSize
		screen.blit(image, drawPos)

		drawPos[0] = posX-text.get_width()//2
		drawPos[1] = posY-text.get_height()//2
		screen.blit(text, drawPos)

		if i == 0:
			if graphics.nextText == None:
				graphics.nextText = font.render("NEXT", True, TEXT_COLOUR)
			drawPos[0] = posX-graphics.nextText.get_width()//2
			drawPos[1] = posY-graphics.nextText.get_height()//2+27
			screen.blit(graphics.nextText, drawPos)

		posX += queueDistance

	drawText()


def drawHealthBar():
	size = gameglobals.size
	screen = gameglobals.screen
	gameStats = gameglobals.gameStats

	# Draw Health Bar
	maxWidth = size[0]*3//4
	rect = pygame.Rect((size[0]-maxWidth)//2,20,maxWidth,20)
	pygame.draw.rect(screen, HPBAR_BACK, rect)
	rect.width *= gameStats.hp
	rect.width //= gameStats.maxHp
	pygame.draw.rect(screen, HPBAR_FRONT, rect)



def drawText():
	screen = gameglobals.screen
	global graphics
	gameStats = gameglobals.gameStats

	value = gameStats.treeSize()
	if graphics.text_treeSize == None or graphics.text_treeSize_value != value:
		graphics.text_treeSize = statsFont.render("Size: " + str(value), True, TEXT_COLOUR)
		graphics.text_treeSize_value = value
	screen.blit(graphics.text_treeSize, [20,30])

	value = gameStats.treeHeight()
	if graphics.text_treeHeight == None or graphics.text_treeHeight_value != value:
		graphics.text_treeHeight = statsFont.render("Height: " + str(value), True, TEXT_COLOUR)
		graphics.text_treeHeight_value = value
	screen.blit(graphics.text_treeHeight, [20,50])


def drawScoreOps():
	screen = gameglobals.screen
	global graphics
	gameStats = gameglobals.gameStats

	value = gameStats.numOperations()
	if graphics.text_operations == None or graphics.text_operations_value != value:
		graphics.text_operations = opsFont.render("Ops: " + str(value), True, OPS_TEXT_COLOUR)
		graphics.text_operations_value = value
	screen.blit(graphics.text_operations, [20,70])


def drawScoreProgress():
	screen = gameglobals.screen
	global graphics
	gameStats = gameglobals.gameStats

	value = gameStats.getFourDigitPercentage()/100
	if graphics.text_operations == None or graphics.text_operations_value != value:
		graphics.text_operations = opsFont.render(str(value)+"%", True, OPS_TEXT_COLOUR)
		graphics.text_operations_value = value
	screen.blit(graphics.text_operations, [20,70])


def drawScoreRotations():
	screen = gameglobals.screen
	global graphics
	gameStats = gameglobals.gameStats
	eventSequence = gameglobals.eventSequence

	value = gameStats.numRotations()
	if graphics.text_operations == None or graphics.text_operations_value != value:
		if value <= eventSequence.gold:
			colour = graphics.TEXTCOLOUR_GOLD
		elif value <= eventSequence.par:
			colour = graphics.TEXTCOLOUR_PAR
		else:
			colour = graphics.TEXTCOLOUR_ABOVEPAR
		graphics.text_operations = opsFont.render("Moves: " + str(value), True, colour)
		graphics.text_operations_value = value
	screen.blit(graphics.text_operations, graphics.rotationsTextPosition)

	if graphics.text_par == None:
		value = eventSequence.par
		graphics.text_par = opsFont.render("Par: " + str(value), True, TEXT_COLOUR)
	screen.blit(graphics.text_par, graphics.parTextPosition)

	if graphics.text_objective == None:
		graphics.text_objective = opsFont.render("OBJECTIVE", True, TEXT_COLOUR)
		width = graphics.text_objective.get_width()
		graphics.objectiveTextPosition[0] = (gameglobals.size[0] - width)//2
	screen.blit(graphics.text_objective, graphics.objectiveTextPosition)


def drawTree(tree):
	screen = gameglobals.screen
	global offset, font, balanceYOffset, graphics

	centerX = gameglobals.cameraCenter[0] + offset[0]
	centerY = gameglobals.cameraCenter[1] + offset[1]

	for edgeLine in tree.edgeLines:
		fromPos = [centerX + edgeLine.fromPosition[0],
			centerY + edgeLine.fromPosition[1]]
		toPos = [centerX + edgeLine.toPosition[0], 
			centerY + edgeLine.toPosition[1]]
		pygame.draw.line(screen, LINE_COLOUR, fromPos, toPos, 3)
		

	drawPos = [0,0] #ignore this statement. I just need a 2-element list.
	arrowIndex = None
	for nodeCircle in tree.nodeCircles:
		balance = tree.balanceOf(nodeCircle)

		positionX = centerX + nodeCircle.position[0]
		positionY = centerY + nodeCircle.position[1]

		if (abs(balance) >= 2):
			drawPos[0] = positionX - graphics.nodeGlowHalfSize
			drawPos[1] = positionY - graphics.nodeGlowHalfSize
			image = graphics.nodeGlow
			screen.blit(image, drawPos)
			if (abs(balance) > 2):
				screen.blit(image, drawPos)


		drawPos[0] = positionX - graphics.nodeHalfSize
		drawPos[1] = positionY - graphics.nodeHalfSize
		if gameglobals.player.isSelected(nodeCircle.index):
			image = graphics.node_selected
			arrowX = positionX
			arrowY = positionY
			arrowIndex = nodeCircle.index
		else:
			image = graphics.node_unselected
		screen.blit(image, drawPos)
		#pygame.draw.circle(screen, colour, position, nodeCircle.radius)

		if (nodeCircle.renderedText == None):
			nodeCircle.renderedText = font.render(
				str(tree.valueOf(nodeCircle)), True, NODE_TEXT_COLOUR)
		drawPos[0] = positionX-nodeCircle.renderedText.get_width()//2
		drawPos[1] = positionY-nodeCircle.renderedText.get_height()//2
		screen.blit(nodeCircle.renderedText, drawPos)

		if (nodeCircle.renderedBalance == None):
			nodeCircle.renderedBalance = font.render(str(balance), True, TEXT_COLOUR)
		drawPos[0] = positionX-nodeCircle.renderedBalance.get_width()//2
		drawPos[1] = positionY-nodeCircle.renderedBalance.get_height()//2 - balanceYOffset
		screen.blit(nodeCircle.renderedBalance, drawPos)

	if arrowIndex != None:
		drawArrow(arrowX, arrowY, arrowIndex)


def drawArrow(nodeX, nodeY, index):
	tree = gameglobals.tree
	screen = gameglobals.screen
	global graphics

	if tree.canRotateRight(index):
		if tree.canRotateLeft(index):
			image = graphics.arrowDouble
		else:
			image = graphics.arrowRight
	else:
		if tree.canRotateLeft(index):
			image = graphics.arrowLeft
		else:
			return
	position = [nodeX + graphics.arrowOffset[0], nodeY + graphics.arrowOffset[1]]
	screen.blit(image, position)


def drawGameOverMessage():
	if not gameglobals.gameStats.gameOver: return
	global graphics
	screen = gameglobals.screen
	size = gameglobals.size
	position = [size[0]//2 - graphics.messageHalfSize[0],
				size[1]//2 - graphics.messageHalfSize[1]]
	screen.blit(graphics.gameOverMessage, position)


def drawTutorialUI():
	drawHealthBar()
	drawStartDialog()
	drawTutorialText()
	drawIntroText()
	drawPromptText()

def drawStandardUI():
	drawHealthBar()
	drawScoreProgress()

def drawEndlessUI():
	drawHealthBar()
	drawScoreOps()

def drawPuzzleUI():
	drawStartDialog()
	drawScoreRotations()
	drawPromptText()


def drawStartDialog():
	global graphics
	if not graphics.dialogOpen: return
	if gameglobals.player.dialogOpen:
		size = gameglobals.size
		rect = pygame.Rect(10, size[1]//2 -45, size[0]-10, 90)
		pygame.draw.rect(gameglobals.screen, [160,30,40], rect)
	else:
		graphics.shiftObjectiveText()
		graphics.shiftObjectiveText = None
		graphics.dialogOpen = False


def drawIntroText():
	global graphics
	if not graphics.dialogOpen: return
	screen = gameglobals.screen
	if graphics.text_objective == None:
		graphics.text_objective = opsFont.render("Welcome to the Tutorial!", True, TEXT_COLOUR)
		width = graphics.text_objective.get_width()
		graphics.objectiveTextPosition[0] = (gameglobals.size[0] - width)//2
	screen.blit(graphics.text_objective, graphics.objectiveTextPosition)


def drawTutorialText():
	if gameglobals.player.currentNode == None: return

	global graphics
	screen = gameglobals.screen
	size = gameglobals.size

	index = gameglobals.player.currentNode.data - 1
	position = [0, size[1] - graphics.tutorialPanelHeight]
	screen.blit(graphics.tutorialImages[index], position)

	if index == 7:
		if graphics.creditsText == None:
			graphics.creditsText = font.render("Made by Oh", True, [170,0,132])
		position = [size[0] - 130, size[1]-35]
		screen.blit(graphics.creditsText, position)


def drawPromptText():
	gameStats = gameglobals.gameStats
	if gameStats.promptTextMessage != None:
		if gameStats.promptText == None:
			global TEXT_COLOUR
			gameStats.promptText = opsFont.render(gameStats.promptTextMessage,
									True, TEXT_COLOUR)
			width = gameStats.promptText.get_width()
			graphics.promptTextPosition[0] = (gameglobals.size[0] - width)//2
		gameglobals.screen.blit(gameStats.promptText, graphics.promptTextPosition)