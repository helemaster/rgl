###########################################################
#main.py
#Base module to run game
#Holly LeMaster, 2017
#Version: Vertical Slice
###########################################################

import libtcodpy as libtcod
import classes
import globs
import globfun

#Constants
LIMIT_FPS = 20

#FOV 
FOV_ALGO = 0    #FOV algorithm to use
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#Population
MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2

###########################################################
#Functions
###########################################################

#Input functions
def handle_keys():
	global key

	#Fullscreen toggle
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	
	#Exit game
	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit'

	#Player can only move if game state is "playing"
	if globs.gameState == 'playing':
		#Movement
		if key.vk == libtcod.KEY_UP:
			playerMoveOrAttack(0, -1)
		elif key.vk == libtcod.KEY_DOWN:
			playerMoveOrAttack(0, 1)
		elif key.vk == libtcod.KEY_LEFT:
			playerMoveOrAttack(-1, 0)
		elif key.vk == libtcod.KEY_RIGHT:
			playerMoveOrAttack(1, 0)
		
		else:
			#Check for other keys
			keyChar = chr(key.c)

			print("handle else")

			if keyChar == 'g':  #Pick up item
				print("pressed g")
				#Look for item in player's tile
				for object in globs.objects: 
					if object.x == globs.player.x and object.y == globs.player.y and object.item:
						object.item.pickUp()
						break

			return 'no-turn'

#Return string with name of objects under mouse
def getNamesUnderMouse():
	global mouse

	(x, y) = (mouse.cx, mouse.cy)

	#Create list with names of objects at mouse coords and in FOV
	names = []
	for obj in globs.objects:
		if obj.x == x and obj.y == y and libtcod.map_is_in_fov(globs.fovMap, obj.x, obj.y):
			names.append(obj.name)

	#Join names into single string, separated by commas
	names = ', '.join(names)

	return names.capitalize()

def playerMoveOrAttack(dx, dy):
	global fovRecompute

	#Coords player is moving to/attacking
	x = globs.player.x + dx
	y = globs.player.y + dy

	#Try to find attackable object at coords
	target = None
	for object in globs.objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break

	#Attack if object found, move otherwise
	if target is not None:   #attack
		globs.player.fighter.attack(target)
	else:
		globs.player.move(dx, dy)
		fovRecompute = True

#Map functions
#Generate 2D map list
def makeMap():

	#Fill map with blocked tiles
	globs.map = [[classes.Tile(True)
			for y in range(classes.MAP_HEIGHT) ]
				for x in range(classes.MAP_WIDTH) ]

	rooms = []
	numRooms = 0

	for r in range(classes.MAX_ROOMS):
		#Randomize width and height
		w = libtcod.random_get_int(0, classes.ROOM_MIN_SIZE, classes.ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, classes.ROOM_MIN_SIZE, classes.ROOM_MAX_SIZE)
		#Randomize position w/o going out of bounds
		x = libtcod.random_get_int(0, 0, classes.MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, classes.MAP_HEIGHT - h - 1)

		newRoom = classes.Rect(x, y, w, h)

		#Check other rooms and see if they intersect with new room
		failed = False
		for otherRoom in rooms:
			if newRoom.getIntersect(otherRoom):
				failed = True
				break

		if not failed:  #No intersections
			#Generate the room
			createRoom(newRoom)
			#Center coords of new room
			(newX, newY) = newRoom.getCenter()

			if numRooms == 0:
				#First room, player starts here
				globs.player.x = newX
				globs.player.y = newY
			else:    #connect new room to existing rooms
				#Get center coords of previous room
				(prevX, prevY) = rooms[numRooms - 1].getCenter()
				#Decide randomly between horizontal vs vertical tunnel
				if libtcod.random_get_int(0, 0, 1) == 1:  #First move horizontally, then vertically
					createHTunnel(prevX, newX, prevY)
					createVTunnel(prevY, newY, newX)
				else:  #first move vertically, then horizontally
					createVTunnel(prevY, newY, prevX)
					createHTunnel(prevX, newX, newY)

			#Populate objects into room
			placeObjects(newRoom)		

			#Append new room to list
			rooms.append(newRoom)
			numRooms += 1

#Create a room
def createRoom(room):
	#Go through tiles in rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			globs.map[x][y].blocked = False
			globs.map[x][y].blockSight = False

#Create horizontal tunnel
def createHTunnel(x1, x2, y):
	for x in range(min(x1, x2), max(x1, x2) + 1):
		globs.map[x][y].blocked = False
		globs.map[x][y].blockSight = False

#Create vertical tunnel
def createVTunnel(y1, y2, x):
	for y in range(min(y1, y2), max(y1, y2) + 1):
		globs.map[x][y].blocked = False
		globs.map[x][y].blockSight = False


#Object functions
#Populate monsters
def placeObjects(room):
	#Choose random number of monsters
	numMonsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

	for i in range(numMonsters):
		#Choose random position for monster
		x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
		y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

		#Only place if tile isn't blocked
		if not globfun.isBlocked(x, y):
			#Determine type of monster & create it
			choice = libtcod.random_get_int(0, 0, 100)
			if choice < 20:
				#Create evil tree w/ fighter component, monster ai, & object
				fighterComponent = classes.Fighter(hp = 10, defense = 4, power = 2, deathFunction = monsterDeath)
				aiComponent = classes.BasicMonster()
				monster = classes.Object(x, y, 't', 'evil tree', libtcod.green, blocks = True, fighter = fighterComponent, ai = aiComponent)  #Tank with little dmg
			elif choice < 20+40:
				fighterComponent = classes.Fighter(hp = 5, defense = 1, power = 2, deathFunction = monsterDeath)
				aiComponent = classes.BasicMonster()
				monster = classes.Object(x, y, 'r', 'rat', libtcod.light_pink, blocks = True, fighter = fighterComponent, ai = aiComponent)   #Weak
			elif choice < 20+40+10:
				fighterComponent = classes.Fighter(hp = 15, defense = 5, power = 4, deathFunction = monsterDeath)
				aiComponent = classes.BasicMonster()
				monster = classes.Object(x, y, 'd', 'buck', libtcod.sepia, blocks = True, fighter = fighterComponent, ai = aiComponent)  #Tank
			else:
				fighterComponent = classes.Fighter(hp = 5, defense = 1, power = 4, deathFunction = monsterDeath)
				aiComponent = classes.BasicMonster()
				monster = classes.Object(x, y, 'h', 'camper', libtcod.desaturated_green, blocks = True, fighter = fighterComponent, ai = aiComponent)  #Glass cannon

			#Add monster to object list
			globs.objects.append(monster)

	#Populate items - choose random number of items
	numItems = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

	for i in range(numItems):
		#Pick random spot for item
		x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
		y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

		#Only place if tile isn't blocked
		if not globfun.isBlocked(x, y):
			#Create HP potion
			itemComponent = classes.Item()
			item = classes.Object(x, y, "!", "healing potion", libtcod.light_red, item = itemComponent)

			globs.objects.append(item)
			item.sendToBack()


#Death handling
#Kill player, change character to corpse, change game state
def playerDeath(player):
	#End game
	globfun.message("You have died!", libtcod.red)
	globs.gameState = "dead"

	#Change player character to corpse
	player.char = '%'
	player.color = libtcod.dark_red

#Kill monster, change character, modify attributes
def monsterDeath(monster):
	globfun.message(monster.name.capitalize() + " is dead!", libtcod.orange)
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.sendToBack()


#Drawing/rendering functions
#Draw all objects in list
def renderAll():
	global fovRecompute

	#Recompute FOV if needed (change occurred)
	if fovRecompute:
		fovRecompute = False
		libtcod.map_compute_fov(globs.fovMap, globs.player.x, globs.player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

	#Render map tiles
	for y in range(classes.MAP_HEIGHT):
		for x in range(classes.MAP_WIDTH):
			visible = libtcod.map_is_in_fov(globs.fovMap, x, y)   #draws tile in different colors depending on its visibility
			wall = globs.map[x][y].blockSight
			if not visible:  #out of player FOV
				if globs.map[x][y].explored:  #Tile can be visible to player only if explored
					if wall:
						libtcod.console_put_char_ex(classes.con, x, y, '#', classes.COLOR_DARK_WALL, libtcod.black)
					else:
						libtcod.console_put_char_ex(classes.con, x, y, '.', classes.COLOR_DARK_GROUND, libtcod.black)
			else:   #Visible
				if wall:
					libtcod.console_put_char_ex(classes.con, x, y, '#', classes.COLOR_LIGHT_WALL, libtcod.black)
				else:
					libtcod.console_put_char_ex(classes.con, x, y, '.', classes.COLOR_LIGHT_GROUND, libtcod.black)
				#Since it's visible, set to explored
				globs.map[x][y].explored = True

	#Render objects (except player - drawn last so it's always on top)
	for object in globs.objects:
		if object != globs.player:
			object.draw()
	globs.player.draw()

	#Push contents of con to root console
	libtcod.console_blit(classes.con, 0, 0, globs.SCREEN_WIDTH, globs.SCREEN_HEIGHT, 0, 0, 0)  


	#Draw GUI elements
	#Prepare for GUI elements
	libtcod.console_set_default_background(globs.panel, libtcod.black)
	libtcod.console_clear(globs.panel)

	#Print messages one line at a time
	y = 1
	for (line, color) in globs.gameMsgs:
		libtcod.console_set_default_foreground(globs.panel, color)
		libtcod.console_print_ex(globs.panel, globs.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1

	#Show player stats
	renderBar(1, 1, globs.BAR_WIDTH, 'HP', globs.player.fighter.hp, globs.player.fighter.maxHP, libtcod.light_red, libtcod.darker_red)

	#Display names of objects under mouse
	libtcod.console_set_default_foreground(globs.panel, libtcod.light_gray)
	libtcod.console_print_ex(globs.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, getNamesUnderMouse())

	#Blit contents of panel to root
	libtcod.console_blit(globs.panel, 0, 0, globs.SCREEN_WIDTH, globs.PANEL_HEIGHT, 0, 0, globs.PANEL_Y)

#Render GUI status bars
def renderBar(x, y, totalWidth, name, value, max, barColor, backColor):
	#Calculate width of the bar
	barWidth = int(float(value) / max * totalWidth)

	#Render background
	libtcod.console_set_default_background(globs.panel, backColor)
	libtcod.console_rect(globs.panel, x, y, totalWidth, 1, False, libtcod.BKGND_SCREEN)

	#Render bar on top of background
	libtcod.console_set_default_background(globs.panel, barColor)
	if barWidth > 0:
		libtcod.console_rect(globs.panel, x, y, barWidth, 1, False, libtcod.BKGND_SCREEN)

	#Render text with values on bar
	libtcod.console_set_default_foreground(globs.panel, libtcod.white)
	libtcod.console_print_ex(globs.panel, x + totalWidth / 2, y, libtcod.BKGND_NONE, libtcod.CENTER, name + ": " + str(value) + "/" + str(max))



###########################################################
#Main game loop & Initialization
###########################################################

#Pre-game set-up
#Variables
fighterComponent = classes.Fighter(hp = 30, defense = 1, power = 5, deathFunction = playerDeath) #Create fighter component for player
globs.player = classes.Object(0, 0, '@', 'player', libtcod.white, blocks = True, fighter = fighterComponent)  #declare player object
globs.objects = [globs.player]  #list holding all active objects

#Set font
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Initialize window
libtcod.console_init_root(globs.SCREEN_WIDTH, globs.SCREEN_HEIGHT, 'mrgl', False)

#Generate map
makeMap()

#Initialize FOV map
globs.fovMap = libtcod.map_new(classes.MAP_WIDTH, classes.MAP_HEIGHT)
for y in range(classes.MAP_HEIGHT):
	for x in range(classes.MAP_WIDTH):
		libtcod.map_set_properties(globs.fovMap, x, y, not globs.map[x][y].blockSight, not globs.map[x][y].blocked)

#Recompute FOV for changes during game
fovRecompute = True

#Set state to playing
globs.gameState = 'playing'

#Initialize GUI panel
globs.panel = libtcod.console_new(globs.SCREEN_WIDTH, globs.PANEL_HEIGHT)

#Print welcoming message
globfun.message("Welcome, stranger! Prepare to perish!", libtcod.lighter_green)

#Mouse and key input handling
mouse = libtcod.Mouse()
key = libtcod.Key()

#Limit FPS
libtcod.sys_set_fps(LIMIT_FPS)

#Main loop
while not libtcod.console_is_window_closed():

	#Check for key presses
	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

	#Render objects & map
	renderAll()
	
	libtcod.console_flush() #Present changes to console

	#Clear objects
	for object in globs.objects:
		object.clear()


	#Key handling
	globs.playerAction = handle_keys()
	
	if globs.playerAction == 'exit':
		break
	

	#Let AIs take turn
	if globs.gameState == 'playing' and globs.playerAction != 'no-turn':
		for object in globs.objects:
			if object.ai:
				object.ai.takeTurn()