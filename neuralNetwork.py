###########################################################
#neuralNetwork.py
#Neural network class
###########################################################

import numpy
import scipy.special as special

#NeuralNet class - representation of a basic neural network
class NeuralNet:
    #Initialize network
    def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
        self.inodes = inputNodes
        self.hnodes = hiddenNodes
        self.onodes = outputNodes
        self.lr = learningRate
        
        #Init random link weight matricies
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        
        #Define anonymous activiation function using lambda shorthand
        self.activation = lambda x: special.expit(x)
        
    #train - trains the neural netwwork
    def train(self, inputsList, targetsList):
        #Convert inputs to 2d numpy array
        inputs = numpy.array(inputsList, ndmin=2).T
        targets = numpy.array(targetsList, ndmin=2).T
        
        #Calculate signals into hidden layer
        hiddenInputs = numpy.dot(self.wih, inputs)
        
        #Apply activation function to signals from hidden layer
        hiddenOutputs = self.activation(hiddenInputs)
        
        #Calculate signals into final output layer
        finalInputs = numpy.dot(self.who, hiddenOutputs)
        
        #Apply activation function to final outputs 
        finalOutputs = self.activation(finalInputs)
        
        #Calculate error: (target - actual)
        #output errors
        outputErrors = targets - finalOutputs
        
        #Backpropagate errors from output layer
        hiddenErrors = numpy.dot(self.who.T, outputErrors)
        
        #Update weights for links between the hidden and output layers
        self.who += self.lr * numpy.dot((outputErrors * finalOutputs * (1.0 - finalOutputs)), numpy.transpose(hiddenOutputs))
        
        #Update weights for links between input and hidden layers
        self.wih += self.lr * numpy.dot((hiddenErrors * hiddenOutputs * (1.0 - hiddenOutputs)), numpy.transpose(inputs))
        
    
    #query - queries the neural network
    #Takes input to neural network and returns network's output
    def query(self, inputsList):
        
        #Convert input list to 2d numpy array
        inputs = numpy.array(inputsList, ndmin=2).T
        
        #Use dot product matrix multiplication to calculate outputs
        #Combines all inputs with link weights to produce a matrix of combined moderated signals into each hidden layer node
        hiddenInputs = numpy.dot(self.wih, inputs)

        #Apply activation function to signals from hidden layer
        hiddenOutputs = self.activation(hiddenInputs)
        
        #Calculate signals into final output layer
        finalInputs = numpy.dot(self.who, hiddenOutputs)
        
        #Calculate signals from final output layer (apply act. func)
        finalOutputs = self.activation(finalInputs)
                
        return finalOutputs