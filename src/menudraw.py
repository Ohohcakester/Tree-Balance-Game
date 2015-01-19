import gameglobals, puzzlelevels 
import pygame, pygame.font
from menucontrol import MenuScreen
pygame.font.init()

BACKGROUND_COLOUR = 0, 0, 0
BUTTON_COLOUR_GLOW = 255, 255, 96
BUTTON_COLOUR_INNER = 32, 96, 224
BUTTON_COLOUR_OUTER = 0, 0, 127
WHITE = 255, 255, 255

drawMenu = [
	lambda screen, selection, renders : drawMenu_main(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_standard(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_endless(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_puzzle(screen, selection, renders)
]

font = pygame.font.SysFont("verdana", 32)
descriptionFont = pygame.font.SysFont("verdana", 18)

class MenuGraphics:

	def __init__(self):
		size = gameglobals.size

		self.background = pygame.image.load("assets/menubg.jpg")
		self.logo = pygame.image.load("assets/logo.png")
		self.logoPos = [(size[0]-self.logo.get_rect()[2])//2, 26]
		
		self.currentMenu = -1
		self.currentOption = -1
		self.descriptionText = None
		self.descriptionTextPosition = [0,gameglobals.size[1]-55]

		self.scoreValue = -2
		self.scoreText = None
		self.scoreTextPosition = [0,gameglobals.size[1]-30]
		self.scoreText2 = None
		self.scoreTextPosition2 = [0,gameglobals.size[1]-30]

		self.TEXTCOLOUR_GOLD = 255, 240, 32
		self.TEXTCOLOUR_PAR = 100, 240, 0
		self.TEXTCOLOUR_ABOVEPAR = 255, 127, 127



graphics = None

def uninitialise():
	global graphics
	graphics = None

def initialise():
	global graphics
	graphics = MenuGraphics()

def drawMenuFrame():
	screen = gameglobals.screen
	global graphics

	screen.fill(BACKGROUND_COLOUR)
	screen.blit(graphics.background, [0,0])

	menu = gameglobals.menu

	currentMenu = menu.currentMenu
	currentOption = menu.currentOption()

	drawMenu[currentMenu](screen, currentOption, menu.optionsTextRender[currentMenu])
	checkSelectionChange(currentMenu, currentOption)
	drawDescriptionText(menu.getDescriptionText())
	drawScoreText(currentMenu, currentOption, menu.getScoreValue())

	pygame.display.flip()

def drawLogo(screen):
	global graphics
	screen.blit(graphics.logo, graphics.logoPos)




def drawMenu_main(screen, selection, renders):
	drawButton(screen, "STANDARD", 0, renders, selection)
	drawButton(screen, "ENDLESS", 1, renders, selection)
	drawButton(screen, "PUZZLE", 2, renders, selection)
	drawButton(screen, "TUTORIAL", 3, renders, selection)
	drawLogo(screen)


def drawMenu_standard(screen, selection, renders):
	drawButton(screen, "EASY", 0, renders, selection)
	drawButton(screen, "NORMAL", 1, renders, selection)
	drawButton(screen, "HARD", 2, renders, selection)
	drawButton(screen, "INSANE", 3, renders, selection)

def drawMenu_endless(screen, selection, renders):
	drawButton(screen, "SURVIVAL", 0, renders, selection)
	drawButton(screen, "BLITZ", 1, renders, selection)
	drawButton(screen, "SUPER BLITZ", 2, renders, selection)

def drawMenu_puzzle(screen, selection, renders):
	for i in range(0,len(renders)):
		drawTileButton(screen, str(i+1), i, renders, selection)


#returns [centerPosition, text]
def generateLongButton(message, index, renders):
	if renders[index] == None:
		renders[index] = font.render(message, True, WHITE)

	nButtons = len(renders)
	x = gameglobals.size[0]//2
	spacing = 100
	y = (gameglobals.size[1] - (nButtons-1)*spacing)//2
	y += index*spacing

	return ([x,y], renders[index])


#generatedButton is [centerPosition, text]
def drawButton(screen, message, index, renders, selection):
	buttonStats = generateLongButton(message, index, renders)
	centerPosition = buttonStats[0]
	text = buttonStats[1]
	halfRectWidth = 150
	halfRectHeight = 35

	rect = pygame.Rect(centerPosition[0]-halfRectWidth,
		centerPosition[1]-halfRectHeight, 2*halfRectWidth, 2*halfRectHeight)

	if (index == selection):
		pygame.draw.rect(screen, BUTTON_COLOUR_GLOW, rect.inflate(10,10))
	pygame.draw.rect(screen, BUTTON_COLOUR_OUTER, rect)
	pygame.draw.rect(screen, BUTTON_COLOUR_INNER, rect.inflate(-5,-5))

	screen.blit(text, [centerPosition[0]-text.get_width()//2,
					centerPosition[1]-text.get_height()//2])


#returns [centerPosition, text]
def generateTileButton(message, index, renders):
	if renders[index] == None:
		renders[index] = font.render(message, True, WHITE)

	cols = gameglobals.menu.tileColumns
	nButtons = len(renders)
	spacing = 100

	x = (gameglobals.size[0] - (cols-1)*spacing)//2
	y = (gameglobals.size[1] - ((nButtons-1)//cols)*spacing)//2
	x += index%cols*spacing
	y += index//cols*spacing

	return ([x,y], renders[index])


#generatedButton is [centerPosition, text]
def drawTileButton(screen, message, index, renders, selection):
	buttonStats = generateTileButton(message, index, renders)
	centerPosition = buttonStats[0]
	text = buttonStats[1]
	halfRectWidth = 35
	halfRectHeight = 35

	rect = pygame.Rect(centerPosition[0]-halfRectWidth,
		centerPosition[1]-halfRectHeight, 2*halfRectWidth, 2*halfRectHeight)

	if (index == selection):
		pygame.draw.rect(screen, BUTTON_COLOUR_GLOW, rect.inflate(10,10))
	pygame.draw.rect(screen, BUTTON_COLOUR_OUTER, rect)
	pygame.draw.rect(screen, BUTTON_COLOUR_INNER, rect.inflate(-5,-5))

	screen.blit(text, [centerPosition[0]-text.get_width()//2,
					centerPosition[1]-text.get_height()//2])

def checkSelectionChange(currentMenu, currentOption):
	if currentMenu != graphics.currentMenu or currentOption != graphics.currentOption:
		graphics.descriptionText = None
		graphics.scoreText = None
		graphics.scoreValue = None
		graphics.currentMenu = currentMenu
		graphics.currentOption = currentOption


def drawDescriptionText(message):
	global graphics
	if graphics.descriptionText == None:
		graphics.descriptionText = descriptionFont.render(message, True, WHITE)
		width = graphics.descriptionText.get_width()
		graphics.descriptionTextPosition[0] = (gameglobals.size[0] - width)//2
	gameglobals.screen.blit(graphics.descriptionText, graphics.descriptionTextPosition)


def drawScoreText(currentMenu, currentOption, scoreValue):
	global graphics
	if scoreValue == None:
		return
	if graphics.scoreText == None or graphics.scoreValue != scoreValue:
		renderScoreMessage(currentMenu, currentOption, scoreValue)
		graphics.scoreValue = scoreValue

	gameglobals.screen.blit(graphics.scoreText, graphics.scoreTextPosition)
	if graphics.scoreText2 != None:
		gameglobals.screen.blit(graphics.scoreText2, graphics.scoreTextPosition2)


def renderScoreMessage(currentMenu, currentOption, scoreValue):
	global graphics

	if currentMenu == MenuScreen.mode_standard:
		message = formatStandard(scoreValue)
		graphics.scoreText = descriptionFont.render(message, True, WHITE)
		width = graphics.scoreText.get_width()
		graphics.scoreTextPosition[0] = (gameglobals.size[0] - width)//2

		graphics.scoreText2 = None

	elif currentMenu == MenuScreen.mode_endless:
		message = formatEndless(scoreValue)
		graphics.scoreText = descriptionFont.render(message, True, WHITE)
		width = graphics.scoreText.get_width()
		graphics.scoreTextPosition[0] = (gameglobals.size[0] - width)//2

		graphics.scoreText2 = None

	elif currentMenu == MenuScreen.mode_puzzle:
		stage = puzzlelevels.getStage(currentOption+1)
		parString = "Par: " + str(stage.par)
		if scoreValue == -1:
			message = "Not Completed"
			colour = WHITE
		else:
			message =  "Best: " + str(scoreValue)
			if scoreValue <= stage.gold:
				colour = graphics.TEXTCOLOUR_GOLD
				parString += "      Gold: " + str(stage.gold)
			elif scoreValue <= stage.par:
				colour = graphics.TEXTCOLOUR_PAR
			else:
				colour = graphics.TEXTCOLOUR_ABOVEPAR

		graphics.scoreText = descriptionFont.render(message, True, colour)
		width = graphics.scoreText.get_width()
		graphics.scoreTextPosition[0] = (gameglobals.size[0])//2 - width- 25

		graphics.scoreText2 = descriptionFont.render(parString, True, WHITE)
		width = graphics.scoreText2.get_width()
		graphics.scoreTextPosition2[0] = (gameglobals.size[0])//2 + 25


def formatStandard(scoreValue):
	if scoreValue == -1:
		scoreValue = 0
	elif scoreValue >= 10000:
		return "CLEAR : 100%"
	return "Progress : " + str(scoreValue/100) + "%"

def formatEndless(scoreValue):
	if scoreValue == -1:
		return "No recorded score"
	return "Score (Ops) : " + str(scoreValue)