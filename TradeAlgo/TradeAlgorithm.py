from Trading212 import Trading212
from DataProcessor import Processor
from helpers import isSet
import pandas as pd
import pandas_ta as pdTa


class TradeAlgorithm:
    def __init__(self, tickers: [str]):
        self.tickers = tickers
        self.processor = Processor(Trading212(useRawRequest=True))

    def getTickers(self):
        return self.tickers

    def getResult(self):
        results = []

        tickerData = []
        for ticker in self.getTickers():
            fetchedData = self.processor.apiInstance.getTickerData(ticker, 'FIVE_MINUTES')

            if not isSet(fetchedData[0], 'response.candles'):
                print(f'No data returned for: {ticker}')
                continue

            tickerData.append(fetchedData[0]['response']['candles'])

        labeledData = [[self.processor.applyDataSchema(data) for data in ticker] for ticker in tickerData]

        return results


