###########################################################
#neuralNetHandler.py
#Interface for NeuralNetwork class
###########################################################

#Global variables

dataContainer = {}

#readData - imports training data from file 
def readData():
	print("--- BEGIN Data Reading ---")
	global dataContainer

	dictEntry = ""
	floorNum = 1

	#Determine number of floors traversed
	floorsTraversed = int(input("How many training files were created? "))

	while floorNum < (floorsTraversed + 1):
		try:
			#Get file name and open
			filename = "nnVars" + str(floorNum) + ".txt"
			nnVarFile = open(filename, "r")
			print("Opened file " + filename + " successfully")

			print("Starting entry construction...")
			#Import and store data
			for line in nnVarFile:
				#Check if this is first pass
				if dictEntry == "":
					dictEntry = line
				else:
					dictEntry += "::" + line

			print("Finished entry construction")
			
			nnVarFile.close()

			#Write floor entry to data dictionary
			dataContainer[floorNum] = dictEntry
			print("Entry written successfully")

			floorNum += 1

		except:
			print("ERR: index out of range")
			print("You entered an invalid number of generated files. Data reading was still completed successfully.")
			break

	print("--- END Data Reading ---")

#train - trains the neural network
def train():
	pass