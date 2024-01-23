import requests
import json


class Trading212:
    VALID_TIME_PERIODS = [
        'ONE_MINUTE',
        'FIVE_MINUTES',
        'TEN_MINUTES',
        'FIFTEEN_MINUTES',
        'THIRTY_MINUTES',
        'ONE_HOUR',
        'FOUR_HOURS',
        'ONE_DAY',
        'ONE_WEEK',
        'ONE_MONTH'
    ]

    TICKER_SCHEMA = ['volume', 'open', 'high', 'low', 'close', 'trades']

    def __init__(self, baseURL: str = 'https://live.trading212.com'):
        self.baseURL = baseURL

    def getValidTimePeriods(self) -> list:
        return self.VALID_TIME_PERIODS

    def getTickerSchema(self) -> list:
        return self.TICKER_SCHEMA

    def makeRequest(self, method: str, endpoint: str, data: dict | None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'live.trading212.com',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        response = None
        match method:
            case 'PUT':
                response = requests.put(f'{self.baseURL}{endpoint}', data=json.dumps(data), headers=headers)

        if response is None or response.status_code != 200:
            raise ConnectionError(f'Error getting data from Trading 212, error: {response.status_code}')

        return response.json()

    def getTickerData(self, ticker: str, timePeriod: str, useAskPrice: bool = False) -> dict:
        """
        The data is returned oldest to newest, in the format: [Volume, Open, High, Low, Close, Trades?]


        :param ticker:
        :param timePeriod:
        :param useAskPrice:
        :return:
        """
        if timePeriod not in timePeriod:
            raise ValueError(f'{timePeriod} is not a valid time period.')

        data = {
            'candles': [
                {
                    'ticker': ticker,
                    'useAskPrice': useAskPrice,
                    'period': timePeriod,
                    'size': 500
                }
            ]
        }

        return self.makeRequest('PUT', '/charting/v3/candles', data)
