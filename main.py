import sys
from Trading212 import Trading212
from DataProcessor import ProcessorV1
import os
from TradeAlgo import TradeAlgorithm


def getData(ticker):
    connection = Trading212()
    responseData = connection.getTickerData(ticker, 'TEN_MINUTES')
    print(responseData)  # use 25 to 45 last periods

    return


def generateData(tickers):
    processor = ProcessorV1(Trading212())
    processor.generateData(tickers, output=os.path.abspath(os.getcwd()) + '/storage/datasets/datasetV1.json')

    return


def getDecision(tickers):
    tradeAlgo = TradeAlgorithm(tickers)

    return tradeAlgo.getResult()


def main():
    arguments = sys.argv

    if len(arguments) == 1:
        return

    match arguments[1]:
        case 'help':
            print('Enter an option to run that function, this was helpful.')
        case 'getData':
            return getData(arguments[2])
        case 'generateData':
            return generateData(arguments[2])
        case 'getDecisions':
            return getDecision(arguments[2].split(','))
        case _:
            print('Option not found')


if __name__ == '__main__':
    main()
