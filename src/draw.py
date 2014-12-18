import gameglobals, pygame, pygame.font
pygame.font.init()

class Graphics:

	def __init__(self):
		self.background = pygame.image.load("bggraphic.png")
		bgRect = self.background.get_rect()
		self.bgHalfSize = [bgRect[2]//2, bgRect[3]//2]
		
		self.node_unselected = pygame.image.load("node.png")
		self.node_selected = pygame.image.load("nodeSelected.png")
		nodeRect = self.node_selected.get_rect()
		self.nodeHalfSize = nodeRect[2]//2

		self.nodeGlow = pygame.image.load("nodeglow.png")
		nodeGlowRect = self.nodeGlow.get_rect()
		self.nodeGlowHalfSize = nodeGlowRect[2]//2

		self.uiBar = pygame.image.load("uibar.png")

		self.addSquare = pygame.image.load("addSquare.png")
		self.deleteSquare = pygame.image.load("deleteSquare.png")
		squareRect = self.addSquare.get_rect()
		self.squareHalfSize = squareRect[2]//2

		self.text_operations = None
		self.text_operations_value = None
		self.text_treeSize = None
		self.text_treeSize_value = None
		self.text_treeHeight = None
		self.text_treeHeight_value = None

		self.nextText = None


	def initialiseTutorialText(self):
		self.tutorialImages = [
			pygame.image.load("tutorialPanel1.png"),
			pygame.image.load("tutorialPanel2.png"),
			pygame.image.load("tutorialPanel3.png"),
			pygame.image.load("tutorialPanel4.png"),
			pygame.image.load("tutorialPanel5.png"),
			pygame.image.load("tutorialPanel6.png"),
			pygame.image.load("tutorialPanel7.png"),
			pygame.image.load("tutorialPanel8.png")]
		self.tutorialPanelHeight = self.tutorialImages[0].get_height()


	def gameOver(self, isVictory):
		self.node_unselected = pygame.image.load("nodeDead.png")
		self.node_selected = pygame.image.load("nodeSelectedDead.png")
		if isVictory:
			self.gameOverMessage = pygame.image.load("victory.png")
		else:
			self.gameOverMessage = pygame.image.load("defeat.png")

		messageRect = self.gameOverMessage.get_rect()
		self.messageHalfSize = [messageRect[2]//2, messageRect[3]//2]


offset = [gameglobals.size[0]//2, gameglobals.size[1]*5//11]
balanceYOffset = 30
normalColours = False

font = pygame.font.SysFont(None, 24)
statsFont = pygame.font.SysFont(None, 20)
opsFont = pygame.font.SysFont(None, 22)
#font = pygame.freetype.Font("font.ttf", 12)

drawOther = lambda : None


def uninitialise():
	global graphics, drawOther
	graphics = None
	normalColours = False
	drawOther = lambda : None


def initialiseTutorial():
	global drawOther
	drawOther = lambda : drawTutorialText()
	graphics.initialiseTutorialText()


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

	drawGameScene()
	drawUI()
	drawGameOverMessage()
	drawOther()

	pygame.display.flip()


def drawUI():
	screen = gameglobals.screen
	global graphics

	gameStats = gameglobals.gameStats
	size = gameglobals.size

	# Draw Frame
	screen.blit(graphics.uiBar, [0,0])

	# Draw Queue
	queue = gameglobals.controller.queue
	operations = queue.nextFewOperations

	queueDistance = 60
	queueSize = len(operations)
	queueLeft = (size[0] - (queueSize-1)*queueDistance)//2
	pos = [queueLeft, 75]

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
		screen.blit(image, [pos[0]-graphics.squareHalfSize,
							pos[1]-graphics.squareHalfSize])

		textPos = [pos[0]-text.get_width()//2,
					pos[1]-text.get_height()//2]
		screen.blit(text, textPos)

		if i == 0:
			if graphics.nextText == None:
				graphics.nextText = opsFont.render("NEXT", True, TEXT_COLOUR)
			textPos = [pos[0]-graphics.nextText.get_width()//2,
						pos[1]-graphics.nextText.get_height()//2+27]
			screen.blit(graphics.nextText, textPos)

		pos[0] += queueDistance


	# Draw Health Bar
	maxWidth = size[0]*3//4
	rect = pygame.Rect((size[0]-maxWidth)//2,20,maxWidth,20)
	pygame.draw.rect(screen, HPBAR_BACK, rect)
	rect.width *= gameStats.hp
	rect.width //= gameStats.maxHp
	pygame.draw.rect(screen, HPBAR_FRONT, rect)


	drawText()


def drawText():
	screen = gameglobals.screen
	global graphics
	gameStats = gameglobals.gameStats

	value = gameStats.numOperations()
	if graphics.text_operations == None or graphics.text_operations_value != value:
		graphics.text_operations = opsFont.render("Ops: " + str(value), True, OPS_TEXT_COLOUR)
		graphics.text_operations_value = value
	screen.blit(graphics.text_operations, [20,70])

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



def drawGameScene():
	screen = gameglobals.screen
	global offset, font, balanceYOffset, graphics

	center = [gameglobals.cameraCenter[0] + offset[0],
		gameglobals.cameraCenter[1] + offset[1]]

	for edgeLine in gameglobals.tree.edgeLines:
		fromPos = [center[0] + edgeLine.fromPosition[0],
			center[1] + edgeLine.fromPosition[1]]
		toPos = [center[0] + edgeLine.toPosition[0], 
			center[1] + edgeLine.toPosition[1]]
		pygame.draw.line(screen, LINE_COLOUR, fromPos, toPos, 3)
		

	for nodeCircle in gameglobals.tree.nodeCircles:
		balance = gameglobals.tree.balanceOf(nodeCircle)

		position = [center[0] + nodeCircle.position[0],
			center[1] + nodeCircle.position[1]]

		if (abs(balance) >= 2):
			circlePos = [position[0] - graphics.nodeGlowHalfSize,
						position[1] - graphics.nodeGlowHalfSize]
			image = graphics.nodeGlow
			screen.blit(image, circlePos)
			if (abs(balance) > 2):
				screen.blit(image, circlePos)


		circlePos = [position[0] - graphics.nodeHalfSize,
					position[1] - graphics.nodeHalfSize]
		if gameglobals.player.isSelected(nodeCircle.index):
			image = graphics.node_selected
		else:
			image = graphics.node_unselected
		screen.blit(image, circlePos)
		#pygame.draw.circle(screen, colour, position, nodeCircle.radius)

		if (nodeCircle.renderedText == None):
			nodeCircle.renderedText = font.render(
				str(gameglobals.tree.valueOf(nodeCircle)), True, NODE_TEXT_COLOUR)
		textPos = [position[0]-nodeCircle.renderedText.get_width()//2,
					position[1]-nodeCircle.renderedText.get_height()//2]
		screen.blit(nodeCircle.renderedText, textPos)

		if (nodeCircle.renderedBalance == None):
			nodeCircle.renderedBalance = font.render(str(balance), True, TEXT_COLOUR)
		textPos = [position[0]-nodeCircle.renderedBalance.get_width()//2,
					position[1]-nodeCircle.renderedBalance.get_height()//2 - balanceYOffset]
		screen.blit(nodeCircle.renderedBalance, textPos)


def drawGameOverMessage():
	if not gameglobals.gameStats.gameOver: return
	global graphics
	screen = gameglobals.screen
	size = gameglobals.size
	position = [size[0]//2 - graphics.messageHalfSize[0],
				size[1]//2 - graphics.messageHalfSize[1]]
	screen.blit(graphics.gameOverMessage, position)



def drawTutorialText():
	global graphics
	screen = gameglobals.screen
	size = gameglobals.size
	index = gameglobals.player.currentNode.data - 1
	position = [0, size[1] - graphics.tutorialPanelHeight]
	screen.blit(graphics.tutorialImages[index], position)

"""
	if graphics.tutorialTexts[textIndex] == None:
		lines = graphics.tutorialTextMessages[textIndex]
		texts = []
		for i in range(0,len(lines)):
			texts.append(font.render(lines[i], True, TEXT_COLOUR, BACKGROUND_COLOUR))
		graphics.tutorialTexts[textIndex] = texts
	else:
		texts = graphics.tutorialTexts[textIndex]

	for i in range(0,len(texts)):
		position = [(size[0] - texts[i].get_width())//2,
					size[1]-100 + 30*i]
		screen.blit(texts[i], position)
"""