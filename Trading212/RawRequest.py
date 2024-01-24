import subprocess
import json


def curl_request(endpoint: str, data: dict, accountType: str = 'demo', method: str = 'PUT'):
    # Define the command to execute using curl
    # data = {"candles":[{"ticker":"EURGBP","useAskPrice":False,"period":"FIVE_MINUTES","size":500}]}
    command = [
        'curl',
        '-X',
        'PUT',
        '-H', 'Accept: application/json',
        '-H', 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8',
        '-H', 'Connection: keep-alive',
        '-H', 'Content-Type: application/json',
        '-H', f'Origin: https://{accountType}.trading212.com',
        '-H', f'Referer: https://{accountType}.trading212.com',
        '-H', 'Accept-Encoding: gzip',
        '--data-raw', f'{json.dumps(data)}',
        '--compressed',
        f'https://{accountType}.trading212.com{endpoint}'
    ]

    # Execute the curl command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Return the stdout of the curl command
    return json.loads(result.stdout)


if __name__ == '__main__':
    response = curl_request('https://demo.trading212.com/charting/v3/candles')
    print(response)
