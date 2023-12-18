import json

from Trading212 import Trading212
from helpers import *


class Processor:
    def __init__(self, apiInstance: Trading212) -> None:
        self.apiInstance = apiInstance

    def getCorrectOutput(self, outputData: list[dict]) -> list:
        return []

    def applyDataSchema(self, tickerData: list) -> dict:
        resultantData = {}
        for key, value in zip(self.apiInstance.getTickerSchema(), tickerData):
            resultantData[key] = value

        return resultantData

    def generateData(
            self,
            tickers: str,
            timePeriod: str = 'FIVE_MINUTES',
            chunkSize: int = 25,
            forwardPoints: int = 3,
            output: str = 'output.json',
            testTrainSplit: float = 0.05  # Meaning 5% is allocated for testing
    ) -> None:
        tickers = tickers.split(',')

        tickerData = []
        for ticker in tickers:
            fetchedData = self.apiInstance.getTickerData(ticker, timePeriod)

            if not isSet(fetchedData[0], 'response.candles'):
                print(f'No data returned for: {ticker}')
                continue

            tickerData.append(fetchedData[0]['response']['candles'])

        labeledData = [[self.applyDataSchema(data) for data in ticker] for ticker in tickerData]

        # Chunk input data
        chunkedData = []
        for ticker in labeledData:
            for n in range(len(ticker) - (1 + chunkSize + forwardPoints)):
                chunkedData.append(ticker[n:n+chunkSize+forwardPoints])

        # Determine correct output
        XData = []
        yData = []
        for datapoint in chunkedData:
            XData.append(datapoint[:(len(datapoint) - forwardPoints)])
            yData.append(self.getCorrectOutput(datapoint[-(forwardPoints + 1):]))

        splitPoint = round(len(XData) * testTrainSplit)
        outputData = {
            'XTrain': XData[splitPoint:],
            'yTrain': yData[splitPoint:],
            'XTest': XData[:splitPoint],
            'yTest': yData[:splitPoint],
        }

        with open(output, 'w') as f:
            json.dump(outputData, f)
            f.close()

        return


class ProcessorV1(Processor):
    def __init__(self, apiInstance: Trading212) -> None:
        super().__init__(apiInstance)

        self.cutoffPercent = 0.0002  # 0.02%
        self.priceField = 'close'

    def getCorrectOutput(self, outputData: list[dict]) -> list:
        """
        This will count any change:
            >cutoffPercent as an increase
            <cutoffPercent as a decrease
            -cutoffPercent < change < cutoffPercent as staying the same

        :param outputData:
        :return:
        """

        priceValues = pluck(outputData, self.priceField)
        changeOverPeriod = getChange(priceValues[0], priceValues[-1])

        outputData = [0 for _ in range(3)]

        if changeOverPeriod < -self.cutoffPercent:
            outputData[0] = 1
        elif changeOverPeriod > self.cutoffPercent:
            outputData[2] = 1
        else:
            outputData[1] = 1

        return outputData
