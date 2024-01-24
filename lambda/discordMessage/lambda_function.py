import requests
import os
import json


def getMessageContent(tradeType, messageData):
    signal, ticker = messageData.split('/')
    url = f'https://{tradeType}.trading212.com/?ticker={ticker}'
    colour = 65340
    if signal == 'SELL':
        colour = 16711680

    discordMessage = {
        "embeds": [
            {
                "type": "rich",
                "description": "Entry point identified",
                "color": colour,
                "url": url,
                "fields": [
                    {
                        "name": "Signal",
                        "value": signal,
                        "inline": False
                    },
                    {
                        "name": "Ticker",
                        "value": ticker,
                        "inline": False
                    },
                    {
                        "name": "Link",
                        "value": url,
                        "inline": False
                    }
                ]
            }
        ]
    }

    return discordMessage

def lambda_handler(event, context):
    discordUrl = 'https://discord.com/api/webhooks/1199342199062659172/dzQzhZ7hpQYmZaK-p0kq2uSqzMrc2IlwdFkclsR5C77RkWzaPVRm_dnOsNywougLRiKF'
    if os.environ.get('DISCORD_URL') is not None:
        discordUrl = os.environ.get('DISCORD_URL')

    tradeType = 'demo'
    if os.environ.get('TRADE_ENVIRONMENT') is not None:
        tradeType = os.environ.get('TRADE_ENVIRONMENT')

    for record in event['Records']:
        payload = record["body"]

        try:
            discordMessage = getMessageContent(tradeType, payload)
        except:
            discordMessage = {
                'content': f'Failed processing payload: {json.dumps(payload)}'
            }

        response = requests.post(discordUrl, json=discordMessage)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
