from .connection import *
from .activation import *


class Node:
    def __init__(self, isInput, isOutput, activation='linear'):
        self.isInput = isInput
        self.isOutput = isOutput
        self.activation = activationFunctions[activation]()

        self.isConnected = False
    
        self.bias = (random.random()*2)-1  # This scales the bias to be between -1 and 1

        self.output = None

    def connect(self):
        self.isConnected = True
    
    def process(self, inputValues):
        summedValues = sum(inputValues) + self.bias
        self.output = self.activation.transform(summedValues)

        return self.output
    
    def mutate(self):
        self.bias = (random.random()*2)-1
    
    def setBias(self, bias):
        self.bias = bias
