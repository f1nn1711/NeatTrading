import random

class Connection:
    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode

        self.weight = (random.random()*2)-1
    
    def feedForward(self):
        inputValue = self.startNode.output

        if not inputValue:
            return None
        
        return inputValue * self.weight
    
    def mutate(self):
        self.weight = (random.random()*2)-1
    
    def setWeight(self, weight):
        self.weight = weight

