###########################################################
#neuralNetHandler.py
#Interface for NeuralNetwork class
###########################################################

#Import libraries
import numpy
from ast import literal_eval
from neuralNetwork import NeuralNet

#Global variables
dataContainer = {}
classifier = ""

#Neural network parameters
INPUT_NODES = 4
HIDDEN_NODES = 30
OUTPUT_NODES = 2
LEARNING_RATE = 0.3

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

def visualizeData():
	print("--- BEGIN VISUALIZATION ---")
	print("")

	
	for key in dataContainer:
		print("File %d:" % key)
		
		data = dataContainer[key].split('::')
		
		for row in data:
			print(row)
		print("")

	print("--- END VISUALIZATION ---")

#train - trains the neural network
def train():
	global dataContainer, classifier
	
	print("--- BEGIN TRAINING ROUTINE ---")

	for key in dataContainer:
		print("Current file: %d" % key)
		records = dataContainer[key]
		records = records.split('::')

		print("Records split successfully")
		
		#Iterate through records and send to classifier
		for row in records:
			data = row.split("&")

			#Convert items from strings
			print("Starting data conversions...")
			count = 0
			while count < len(data):
				strr = data[count]
				print("strr: " + str(strr))
				if data[count].endswith(")"):  #Convert tuple
					strr.translate(None, '()')  #Remove parentheses
					strr = literal_eval(strr)   #Convert from string to tuple
					data[count] = strr
				else:
					strr = int(strr)
					data[count] = strr 
				count += 1
			print("Data conversion successful")

			target = data[1]  #Get stairs pos tuple

			#Remove target from data & convert to numpy array
			data.pop(1)

			count = 0
			while count < len(data):
				if not isinstance(data[count], tuple):
					print(data[count])
					data[count] = (data[count], None)
					print(data[count])
				count += 1

			inputs = numpy.asfarray(data, dtype=object)

			print("Data split successfully")

			#Send data to classifier
			classifier.train(inputs, target)

			print("Classifier trained successfully")
	print("--- END TRAINING ROUTINE ---")
	 
def predict():
	pass

def menu():
	print("--- Neural Network Handler ---")
	print("1) Visualize data")
	print("2) Read data")
	print("3) Train neural network")
	print("4) Test predictions")
	print("5) Quit")
	print("")

def main():
	go = True

	while go:
		menu()

		try:
			choice = int(input("Enter selection: "))
		except:
			print("Invalid input!")
			choice = 999

		#Check choice
		if(choice == 1):
			print("Visualizing data...")
			print("")
			visualizeData()
			print("")
		elif(choice == 2):
			print("Reading data...")
			print("")
			readData()
			print("")
		elif(choice == 3):
			print("Training neural network...")
			print("")
			train()
			print("")
		elif(choice == 4):
			print("Testing predictions...")
			print("")
			predict()
			print("")
		elif(choice == 5):
			print("Goodbye.")
			print("")
			go = False
		else:
			print("Invalid choice! Try again.")
			print("")

######################################
#Instantiate neural network class
classifier = NeuralNet(INPUT_NODES, HIDDEN_NODES, OUTPUT_NODES, LEARNING_RATE)

#Run menu
main()