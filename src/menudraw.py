import gameglobals, pygame, pygame.font
pygame.font.init()

BACKGROUND_COLOUR = 0, 0, 0
BUTTON_COLOUR_GLOW = 255, 255, 0
BUTTON_COLOUR_INNER = 0, 64, 255
BUTTON_COLOUR_OUTER = 0, 0, 127
WHITE = 255, 255, 255

drawMenu = [
	lambda screen, selection, renders : drawMenu_main(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_standard(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_endless(screen, selection, renders),
	lambda screen, selection, renders : drawMenu_puzzle(screen, selection, renders)
]

font = pygame.font.SysFont("verdana", 32)

class MenuGraphics:

	def __init__(self):
		self.background = pygame.image.load("assets/menubg.png")


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
	drawMenu[menu.currentMenu](screen, menu.currentOption(), 
		menu.optionsTextRender[menu.currentMenu])
	pygame.display.flip()


def drawMenu_main(screen, selection, renders):
	drawButton(screen, "STANDARD", 0, renders, selection)
	drawButton(screen, "ENDLESS", 1, renders, selection)
	drawButton(screen, "PUZZLE", 2, renders, selection)
	drawButton(screen, "TUTORIAL", 3, renders, selection)


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