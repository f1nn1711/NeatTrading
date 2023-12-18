from nnets.neuralNetwork import NeuralNetwork


class Agent:
    def __init__(self, networkInputs=1, networkOutputs=1, outputActivation='sigmoid', jsonData=None):
        if jsonData:
            self.neuralNetwork = NeuralNetwork(networkJson=jsonData)
            return

        self.neuralNetwork = NeuralNetwork(networkInputs, networkOutputs, outputActivation)

    def addNode(self, addConn):
        newNode = self.neuralNetwork.addNode()

        if addConn:
            self.addConnection(endNode=newNode)
            self.addConnection(startNode=newNode)

        return newNode

    def addConnection(self, startNode=None, endNode=None):
        return self.neuralNetwork.addConnection(startNode, endNode)

    def getNetworkResponse(self, inputs):
        return self.neuralNetwork.run(inputs)

    def setFitness(self, fitness):
        self.fitness = fitness

    def getConnections(self):
        return self.neuralNetwork.getConnections()

    def getNodes(self):
        return self.neuralNetwork.getNodes()
