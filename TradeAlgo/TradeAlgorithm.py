from Trading212 import Trading212
from DataProcessor import Processor
from helpers import isSet
import pandas as pd
import pandas_ta as pdTa
import MessageHandler
import json
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PyTrading212 import CFD, CFDOrder
from PyTrading212 import Mode


RESULT_VALUES = {
    '-1': 'SELL',
    '0': 'NA',
    '1': 'BUY'
}


def getCurrentCalls() -> list:
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/currentCalls.json', 'r') as f:
            currentCalls = json.loads(f.read())
            f.close()
    except Exception as e:
        logging.error(f'Unable to get current calls, error: {e}')

        return []

    return currentCalls['calls']


def setCurrentCalls(calls: list[str]) -> None:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/currentCalls.json', 'w') as f:
        currentCallsData = {
            'calls': [call for call in calls]
        }

        f.write(json.dumps(currentCallsData))
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
            logging.info(f'Getting data for: {ticker}')
            fetchedData = self.processor.apiInstance.getTickerData(ticker, 'FIVE_MINUTES')

            if not isSet(fetchedData[0], 'response.candles'):
                logging.error(f'No data returned for: {ticker}, skipping')
                continue

            tickerData.append(fetchedData[0]['response']['candles'])

        try:
            labeledData = [[self.processor.applyDataSchema(data) for data in ticker] for ticker in tickerData]
            logging.info(f'Processed data in to analytic format')
        except Exception as e:
            logging.critical(f'Unable to process data in to usable format: {e}')
            quit()

        handler = MessageHandler.Messager()
        tradeExecuter = TradeExecuter()
        currentCalls = getCurrentCalls()
        for ticker, data in zip(self.getTickers(), labeledData):
            result = self.getTickerResult(ticker, data)
            logging.info(f'Got result {result}({RESULT_VALUES[str(result)]}) for {ticker}')

            if result == 0:
                filteredCalls = []
                for call in currentCalls:
                    if ticker in call:
                        continue

                    filteredCalls.append(call)

                currentCalls = filteredCalls

            if result == -1 and f'SELL/{ticker}' not in currentCalls:
                logging.info(f'Making sell call for {ticker}')

                handleTrade(f'SELL/{ticker}', handler, tradeExecuter)
                currentCalls.append(f'SELL/{ticker}')

                if f'BUY/{ticker}' in currentCalls:
                    currentCalls.remove(f'BUY/{ticker}')

                logging.info(f'Finished sell call for {ticker}')

                continue

            if result == 1 and f'BUY/{ticker}' not in currentCalls:
                logging.info(f'Making buy call for {ticker}')

                handleTrade(f'BUY/{ticker}', handler, tradeExecuter)
                currentCalls.append(f'BUY/{ticker}')

                if f'SELL/{ticker}' in currentCalls:
                    currentCalls.remove(f'SELL/{ticker}')

                logging.info(f'Finished buy call for {ticker}')

                continue

        if tradeExecuter.shouldExecute():
            tradeExecuter.executeAll()

        setCurrentCalls(currentCalls)

        return results

    def getTickerResult(self, ticker: str, data: list) -> int:
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


class TradeExecuter:
    def __init__(self):
        self.calls = []

    def addCall(self, call: str):
        self.calls.append(call)

    def shouldExecute(self):
        return bool(self.calls)

    def executeAll(self):
        driver = webdriver.Chrome(service=Service())
        cfd = CFD(email=os.environ['PLATFORM_EMAIL'], password=os.environ['PLATFORM_PASSWORD'], driver=driver, mode=Mode.DEMO)

        for call in self.calls:
            signal, ticker = call.split('/')
            cfd_order = CFDOrder(
                instrument_code=ticker,
                quantity=-0.1,  # Sell (quantity is negative)
                target_price=cfd.get_current_price(instrument_code=ticker)
            )

            print(cfd.execute_order(order=cfd_order))

        return

def handleTrade(
        call: str,
        messageHandler: MessageHandler.Messager | None = None,
        tradeExecuter: TradeExecuter | None = None
) -> None:
    if os.environ['EXECUTE_TRADES'] == 'True':
        tradeExecuter.addCall(call)

        return

    messageHandler.enqueue(call, 'MessageQueue-dev')
