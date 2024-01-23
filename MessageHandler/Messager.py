import boto3
import hashlib
import time


class Messager:
    def __init__(self, profile: str = 'personal'):
        self.session = boto3.Session(profile_name=profile)

    def enqueue(self, message: str, queue: str, group: str = 'default'):
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

        return response


if __name__ == '__main__':
    handler = Messager()
    handler.enqueue('BUY/EURGBP', 'MessageQueue-dev')
