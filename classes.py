###########################################################
#classes.py
#Contains main classes
###########################################################

import libtcodpy as libtcod
import globs
import globfun
import math

#Constants
#Size of map
MAP_WIDTH = 80
MAP_HEIGHT = 43

#Room sizes/limits
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

#Declare colors for map tiles
COLOR_DARK_WALL = libtcod.Color(0, 0, 100)
COLOR_DARK_GROUND = libtcod.Color(50, 50, 150)
COLOR_LIGHT_WALL = libtcod.Color(50, 50, 150)
COLOR_LIGHT_GROUND = libtcod.Color(200, 180, 50)

#Inventory capacity
INVENTORY_SIZE = 26

#Other constants
CONFUSE_TURNS = 10

#Variables
#Create main off-screen console
con = libtcod.console_new(globs.SCREEN_WIDTH, globs.SCREEN_HEIGHT)


###########################################################
###########################################################
#OBJECT CLASSES
###########################################################
###########################################################

###########################################################
#Object - generic object, always represented by character
###########################################################
class Object:
	def __init__(self, x, y, char, name, color, blocks = False, alwaysVisible = False, fighter = None, ai = None, item = None, equipment = None):
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.blocks = blocks
		self.alwaysVisible = alwaysVisible
		self.color = color

		#Components
		self.fighter = fighter
		if self.fighter:   #Let fighter component know who owns it
			self.fighter.owner = self
		
		self.ai = ai
		if self.ai:
			self.ai.owner = self

		self.item = item
		if self.item:
			self.item.owner = self

		self.equipment = equipment
		if self.equipment:
			self.equipment.owner = self
			self.item = Item()   #Auto make item component since equipment must be an item
			self.item.owner = self

	def __str__(self):
		return self.name

	#Functions
	#Move character by given amount
	def move(self, dx, dy):
		#Make sure wall isn't in way
		if not globfun.isBlocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy

	#Set color and draw character for object
	def draw(self):
		#Only show object if it's visible to player
		if(libtcod.map_is_in_fov(globs.fovMap, self.x, self.y) or (self.alwaysVisible and globs.map[self.x][self.y].explored)):
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	#Erase character
	def clear(self):
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

	#Move toward a specified object
	def moveToward(self, targetX, targetY):
		#Vector from this object to target, and get distance
		dx = targetX - self.x
		dy = targetY - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#Normalize to length 1 (preserving direction), round, convert to integer
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		self.move(dx, dy)

	#Get distance from object to another object
	def distanceTo(self, other):
		dx = other.x - self.x
		dy = other.y - self.y

		return math.sqrt(dx ** 2 + dy ** 2)

	#Get distance from object to a tile
	def distance(self, x, y):
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

	#Make this object drawn first (on bottom)
	def sendToBack(self):
		globs.objects.remove(self)
		globs.objects.insert(0, self)

	#Get buffer console
	def getCon(self):
		return con


###########################################################
###########################################################
#MAP CLASSES
###########################################################
###########################################################

###########################################################
#Tile - tile of map
###########################################################
class Tile:
	def __init__(self, blocked, blockSight = None):
		self.blocked = blocked
		self.explored = False   #Whether a tile has been explored before by player

		#If tile is blocked it also blocks sight
		if blockSight is None: blockSight = blocked
		self.blockSight = blockSight

###########################################################
#Rect - rectangle room on map
###########################################################
class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def getCenter(self):
		centerX = (self.x1 + self.x2) / 2
		centerY = (self.y1 + self.y2) / 2
		return (centerX, centerY)

	#Returns true if this rect intersects with another one
	def getIntersect(self, other):
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)



###########################################################
###########################################################
#COMPONENT CLASSES
###########################################################
###########################################################

###########################################################
#Fighter - combat properties and methods component
###########################################################
class Fighter:
	def __init__(self, hp, defense, power, xp, deathFunction = None):
		self.maxHP = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.xp = xp
		self.deathFunction = deathFunction

	def takeDamage(self, damage):
		#Apply damage, if possible
		if damage > 0:
			self.hp -= damage

		#Check if object is dead
		if self.hp <= 0:
			function = self.deathFunction
			if function is not None:
				function(self.owner)

			#Give xp for player
			if self.owner != globs.player:
				globs.player.fighter.xp += self.xp

		
	def attack(self, target):
		#Simple formula for attack damage
		damage = self.power - target.fighter.defense

		if damage > 0:
			globfun.message(self.owner.name.capitalize() + " attacks " + target.name + " for " + str(damage) + " hit points.", libtcod.white)
			target.fighter.takeDamage(damage)
		else:
			globfun.message(self.owner.name.capitalize() + " attacks " + target.name + " but it has no effect!", libtcod.white)

	#Heal by given amount w/o going over maximum
	def heal(self, amount):
		self.hp += amount
		if self.hp > self.maxHP:
			self.hp = self.maxHP

#Monster behavior components
###########################################################
#BasicMonster - basic monster AI
###########################################################
class BasicMonster:
	def takeTurn(self):
		#If player can see monster it can see the player
		monster = self.owner

		if libtcod.map_is_in_fov(globs.fovMap, monster.x, monster.y):
			#Move toward player if far away
			if monster.distanceTo(globs.player) >= 2:
				monster.moveToward(globs.player.x, globs.player.y)
			#Attack if close enough (if player is alive)
			elif globs.player.fighter.hp > 0:
				monster.fighter.attack(globs.player)

###########################################################
#ConfusedMonster - monster manupilated by a spell
###########################################################
class ConfusedMonster:
	def __init__(self, oldAI, numTurns = CONFUSE_TURNS):
		self.oldAI = oldAI
		self.numTurns = numTurns

	def takeTurn(self):
		if self.numTurns > 0:   #Still confused
			#Move randomly and decrease number of turns confused
			self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			self.numTurns -= 1
		else:
			#Restore previous AI
			self.owner.ai = self.oldAI
			globfun.message("The" + self.owner.name + " snaps out of confusion!", libtcod.orange) 

###########################################################
#Item - can be picked up & used
###########################################################
class Item:
	def __init__(self, useFunction = None):
		self.useFunction = useFunction  #What the item does

	#Add to player's inventory and remove from map
	def pickUp(self):
		if len(globs.inventory) >= INVENTORY_SIZE:
			globfun.message("Your can't fit anything else into your bag.", libtcod.red)
		else:
			globs.inventory.append(self.owner)
			globs.objects.remove(self.owner)
			globfun.message("Aquired a " + self.owner.name + ".", libtcod.green)

	#Use item - call its useFunction if defined
	def use(self):
		if self.useFunction is None:
			globfun.message("The " + self.owner.name + " cannot be used.")
		else:
			if self.useFunction != "cancelled":
				globs.inventory.remove(self.owner)  #Consume after use unless it was cancelled
				self.useFunction()

	#Drop an item to the ground below player
	def drop(self):
		globs.objects.append(self.owner)
		globs.inventory.remove(self.owner)
		self.owner.x = globs.player.x
		self.owner.y = globs.player.y
		globfun.message("You dropped a " + self.owner.name + ".", libtcod.yellow)

###########################################################
#Equipment - can be equipped & yields bonuses
###########################################################
class Equipment:
	def __init__(self, slot):
		self.slot = slot
		self.isEquipped = False

	#Toggle quip/dequip status
	def toggleEquip(self):
		if self.isEquipped:
			self.dequip()
		else:
			self.equip()

	#Equip item and show a message about it
	def equip(self):
		self.isEquipped = True
		globfun.message("Equipped " + self.owner.name + " on " + self.slot + ".", libtcod.light_green)

	#Dequip equipment and display a message
	def dequip(self):
		if not self.isEquipped: return
		self.isEquipped = False
		globfun.message("Dequipped " + self.owner.name + " from " + self.slot + ".", libtcod.light_yellow)

###########################################################
###########################################################
#MISCELLANEOUS FUNCTIONS
###########################################################
###########################################################

