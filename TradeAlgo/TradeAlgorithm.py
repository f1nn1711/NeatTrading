from Trading212 import Trading212
from DataProcessor import Processor
from helpers import isSet
import pandas as pd
import pandas_ta as pdTa
import MessageHandler
import json



def checkIfCallExists(callCode: str) -> bool:
    with open('./TradeAlgo/data/currentCalls.json', 'r') as f:
        currentCalls = json.loads(f.read())
        f.close()

    if callCode in currentCalls['calls']:
        return True

    return False


def updateCurrentCalls(callCode: str) -> None:
    with open('./TradeAlgo/data/currentCalls.json', 'r') as f:
        currentCalls = json.loads(f.read())
        f.close()

    with open('./TradeAlgo/data/currentCalls.json', 'w') as f:
        currentCalls['calls'].append(callCode)

        f.write(json.dumps(currentCalls))
        f.close()

def removeCurrentCall(callCode: str) -> None:
    with open('./TradeAlgo/data/currentCalls.json', 'r') as f:
        currentCalls = json.loads(f.read())
        f.close()

    with open('./TradeAlgo/data/currentCalls.json', 'w') as f:
        currentCalls['calls'].remove(callCode)

        f.write(json.dumps(currentCalls))
        f.close()


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
            print(f'Getting data for: {ticker}')
            fetchedData = self.processor.apiInstance.getTickerData(ticker, 'FIVE_MINUTES')

            if not isSet(fetchedData[0], 'response.candles'):
                print(f'No data returned for: {ticker}')
                continue

            tickerData.append(fetchedData[0]['response']['candles'])

        labeledData = [[self.processor.applyDataSchema(data) for data in ticker] for ticker in tickerData]
        print(f'Processed data in to analytic format')

        handler = MessageHandler.Messager()
        print('Started the message handler')
        callsMade = []
        for ticker, data in zip(self.getTickers(), labeledData):
            print(f'Getting result for: {ticker}')
            result = self.getTickerResult(ticker, data)
            print(f'Got result {result} for {ticker}')
            if result == -1 and not checkIfCallExists(f'SELL/{ticker}'):
                print(f'Making sell call for {ticker}')
                handler.enqueue(f'SELL/{ticker}', 'MessageQueue-dev')
                updateCurrentCalls(f'SELL/{ticker}')
                print(f'Finished sell call for {ticker}')
                continue

            if result == 1 and not checkIfCallExists(f'BUY/{ticker}'):
                print(f'Making buy call for {ticker}')
                handler.enqueue(f'BUY/{ticker}', 'MessageQueue-dev')
                updateCurrentCalls(f'BUY/{ticker}')
                print(f'Finished buy call for {ticker}')
                continue

            if result == 0:
                print('Checking if calls need to be removed')
                try:
                    if checkIfCallExists(f'BUY/{ticker}'):
                        removeCurrentCall(f'BUY/{ticker}')
                        continue

                    if checkIfCallExists(f'SELL/{ticker}'):
                        removeCurrentCall(f'SELL/{ticker}')
                except Exception as e:
                    print(e)

        return results

    def getTickerResult(self, ticker: str, data: list) -> int:
        #if ticker == 'NZDUSD':
        #    return 1

        df = pd.DataFrame.from_dict(data)

        strategy = pdTa.Strategy('Strategy v1', ta=[
            {"kind": "adx", "length": 14},
            {"kind": "rsi", "length": 14},
            {"kind": "bbands", "length": 20, "std": 2}
        ])

        df.ta.strategy(strategy)

        adxValue = float(df.tail(1)['ADX_14'].iloc[0])
        if adxValue < 25:
            return 0

        currentPrice = float(df.tail(1)['close'].iloc[0])
        bbUpper = float(df.tail(1)['BBU_20_2.0'].iloc[0])
        bbLower = float(df.tail(1)['BBL_20_2.0'].iloc[0])
        rsiValue = float(df.tail(1)['RSI_14'].iloc[0])

        if rsiValue <= 30 and currentPrice < bbLower:
            return 1

        if rsiValue >= 70 and currentPrice > bbUpper:
            return -1

        return 0


