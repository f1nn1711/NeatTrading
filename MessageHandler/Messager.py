import boto3
import hashlib
import time
import os


class Messager:
    def __init__(self, profile: str = 'personal'):
        self.session = boto3.Session(
            os.environ['AWS_ACCESS_KEY_ID'],
            os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ['AWS_REGION']
        )

    def enqueue(self, message: str, queue: str, group: str = 'default'):
        print(f'Trying to send message: {message} to {queue}')
        client = self.session.client('sqs')

        response = client.list_queues(
            QueueNamePrefix=queue
        )

        if len(response['QueueUrls']) != 1:
            raise ValueError(f'{len(response)} queues returned.')

        response = client.send_message(
            QueueUrl=response['QueueUrls'][0],
            MessageBody=message,
            MessageGroupId=group,
            MessageDeduplicationId=hashlib.sha256(f'{message}{time.time()}'.encode()).hexdigest()
        )

        try:
            print(f'Sent message, status code: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        except:
            print('Failed processing response')

        return response


if __name__ == '__main__':
    handler = Messager()
    handler.enqueue('BUY/EURGBP', 'MessageQueue-dev')
