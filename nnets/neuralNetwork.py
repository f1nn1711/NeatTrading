from .node import *
from .connection import *
import random
import json
import os
import time


class NeuralNetwork:
    def __init__(self, nInput=1, nOutput=1, outputActivation='linear', networkJson=None):
        if networkJson:
            self.loadNetworkFromJson(networkJson)
            return

        self.nInput = nInput
        self.nOutput = nOutput
        self.outputActivation = outputActivation
        self.inputNodes = []
        self.hiddenNodes = []
        self.outputNodes = []
        self.connections = []
        self.generateNodes()

    def generateNodes(self):
        for n in range(self.nInput):
            self.inputNodes.append(Node(True, False))

        for n in range(self.nOutput):
            self.outputNodes.append(Node(False, True, self.outputActivation))

    def addNode(self, isInput=False, inOutput=False, activation='linear'):
        newNode = Node(isInput, inOutput, activation)
        self.hiddenNodes.append(newNode)

        return newNode

    def addConnection(self, startNode=None, endNode=None):
        if startNode and endNode:
            newConnection = Connection(startNode, endNode)
        else:
            if not startNode:
                fromNodes = self.inputNodes + self.hiddenNodes
                startNode = random.choice(fromNodes)

            if not endNode:
                toNodes = self.outputNodes + self.hiddenNodes

                isValid = False
                while not isValid:
                    endNode = random.choice(toNodes)

                    if endNode != startNode:
                        isValid = True

            newConnection = Connection(startNode, endNode)

        self.connections.append(newConnection)

    def run(self, inputs):
        # map the inputs to all the input nodes
        for node, inputValue in zip(self.inputNodes, inputs):
            node.process([inputValue])

        continueFProp = True
        # While not finished
        while continueFProp:
            # Loop through each node that isn't an input node
            for node in self.hiddenNodes + self.outputNodes:
                # Get the connections where to toNode is the
                relevantConnections = []
                for connection in self.connections:
                    if connection.endNode == node:
                        relevantConnections.append(connection)

                feedForwardResults = []
                # Try to do feedForward on each of the connections
                fullFeedForward = True
                for connection in relevantConnections:
                    # print(f'Node: {n1} Connection: {n2}')
                    if (result := connection.feedForward()) is not None:
                        feedForwardResults.append(result)
                    else:
                        fullFeedForward = False
                        break

                # if feedForward can be done on all the connection
                if fullFeedForward:
                    # pass the results of all of the feedForwards in to the input of the node
                    # run the node to set its output
                    node.process(feedForwardResults)

            # Loop through all of the output nodes and see of they have outputs
            gotAllResults = True
            networkOutput = []
            for node in self.outputNodes:
                if result := node.output:
                    networkOutput.append(result)
                else:
                    gotAllResults = False
                    break

            # If all of them have outputs break out of while
            if gotAllResults:
                continueFProp = False

        # set the outputs of all of them to None
        for node in self.hiddenNodes:
            node.output = None

        for node in self.outputNodes:
            node.output = None

        # return all the output values
        return networkOutput

    def networkInfo(self):
        print('-' * 40)
        print(f'Input nodes: {len(self.inputNodes)}')
        print(f'Hidden nodes: {len(self.hiddenNodes)}')
        print(f'Output nodes: {len(self.outputNodes)}')
        print(f'Connections: {len(self.connections)}')
        print('')
        tunableParams = len(self.connections) + len(self.outputNodes) + len(self.hiddenNodes) + len(self.inputNodes)
        print(f'Tunable Parameters: {tunableParams}')
        print('-' * 40)

    def getConnections(self):
        return self.connections

    def getNodes(self):
        return self.inputNodes + self.hiddenNodes + self.outputNodes

    def getNetworkJSON(self):
        networkDict = {
            "nodes": [],
            "connections": []
        }

        networkNodes = self.outputNodes + self.hiddenNodes + self.inputNodes
        for node in networkNodes:
            nodeDict = {
                "isOutput": node.isOutput,
                "isInput": node.isInput,
                "activation": node.activation.name,
                "bias": node.bias
            }

            networkDict["nodes"].append(nodeDict)

        for connection in self.connections:
            connectionDict = {
                "start": networkNodes.index(connection.startNode),
                "end": networkNodes.index(connection.endNode),
                "weight": connection.weight
            }

            networkDict["connections"].append(connectionDict)

        return json.dumps(networkDict)

    def loadNetworkFromJson(self, networkJson):
        self.nInput = 0
        self.nOutput = 0
        self.outputActivation = 'linear'
        self.inputNodes = []
        self.hiddenNodes = []
        self.outputNodes = []
        self.connections = []

        for node in networkJson['nodes']:
            if node['isInput']:
                newNode = Node(True, False, node['activation'])
                newNode.setBias(node['bias'])
                self.inputNodes.append(newNode)
            elif node['isOutput']:
                newNode = Node(False, True, node['activation'])
                newNode.setBias(node['bias'])

                self.outputNodes.append(newNode)
            else:
                newNode = Node(False, False, node['activation'])
                newNode.setBias(node['bias'])

                self.hiddenNodes.append(newNode)

        self.nInput = len(self.inputNodes)
        self.nOutput = len(self.outputNodes)

        networkNodes = self.outputNodes + self.hiddenNodes + self.inputNodes
        for connection in networkJson['connections']:
            newConnection = Connection(networkNodes[connection['start']], networkNodes[connection['end']])
            newConnection.setWeight(connection['weight'])
            self.connections.append(newConnection)

    def saveNetwork(self, path='saves/', prefix=''):
        fileName = prefix + str(round(time.time())) + '.json'
        fileData = self.getNetworkJSON()

        with open(path + fileName, 'w') as f:
            f.write(fileData)
            f.close()

