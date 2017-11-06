###########################################################
#globfun.py
#Store global functions for use in multiple files
###########################################################

import libtcodpy as libtcod
import globs
import textwrap

#Global functions

#Check if a tile is blocked by object
def isBlocked(x, y):
	#Test map tile
	if globs.map[x][y].blocked:
		return True

	#Check for blocking objects
	for object in globs.objects:
		if object.blocks and object.x == x and object.y == y:
			return True

	return False


#Create and render game messages
def message(newMsg, color = libtcod.white):
	#Split message among multiple lines if needed
	newMsgLines = textwrap.wrap(newMsg, globs.MSG_WIDTH)

	for line in newMsgLines:
		#If message buffer is full, remove first line to make room for next
		if len(globs.gameMsgs) == globs.MSG_HEIGHT:
			del globs.gameMsgs[0]

		#Add new line as tuple w/ text and color
		globs.gameMsgs.append( (line, color) )

#Check equipment slots and return items in them
def getEquippedInSlot(slot):
	for obj in globs.inventory:
		if obj.equipment and obj.equipment.slot == slot and obj.equipment.isEquipped:
			return obj.equipment
	return None

#Get all equipped
def getAllEquipped(obj):
	if obj == globs.player:
		equippedList = []
		for item in globs.inventory:
			if item.equipment and item.equipment.isEquipped:
				equippedList.append(item.equipment)
		return equippedList
	else:
		return []

