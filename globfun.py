###########################################################
#globfun.py
#Store global functions for use in multiple files
###########################################################

import globs

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


