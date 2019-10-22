###########################################################
#globs.py
#Store global variables for use in multiple files
###########################################################

#Global constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
PANEL_HEIGHT = 7
BAR_WIDTH = 20
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

#Global variables

map = ""      #Map array for tiles
fovMap = ""   #libtcod's FOV map
gameState = ""    #State of game
playerAction = "declared"   #Player's action
objects = []   #List to store all objects in game
player = ""  #Object that holds player
panel = []  #GUI panel
gameMsgs = []  #List of game messages - message and its color
inventory = []  #Player inventory
money = 0


