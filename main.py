import sys
from neat import NEAT
import json
from Trading212 import Trading212
from DataProcessor import ProcessorV1
import os


def train():
    print('Generating population')
    with open('config.json', 'r') as file:
        config = json.loads(file.read())

    controller = NEAT(config)
    # for each gen
    #   for each agent
    #       agent.getNetworkResponse(obs)
    #       set the fitness of the agent
    #   call generateEvolvedPopulation to set new population

    return


def getData(ticker):
    connection = Trading212()
    responseData = connection.getTickerData(ticker, 'TEN_MINUTES')
    print(responseData)  # use 25 to 45 last periods

    return


def generateData(tickers):
    processor = ProcessorV1(Trading212())
    processor.generateData(tickers, output=os.path.abspath(os.getcwd()) + '/storage/datasets/datasetV1.json')

    return


def main():
    arguments = sys.argv

    if len(arguments) == 1:
        return

    match arguments[1]:
        case 'train':
            return train()
        case 'help':
            print('Enter an option to run that function, this was helpful.')
        case 'getData':
            return getData(arguments[2])
        case 'generateData':
            return generateData(arguments[2])
        case _:
            print('Option not found')


if __name__ == '__main__':
    main()
