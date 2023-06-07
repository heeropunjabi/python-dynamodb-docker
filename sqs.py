import boto3
from logzero import logger
import json

sqs = None


def connect_sqs():
    global sqs
    sqs = boto3.resource('sqs',
                         endpoint_url='http://localhost:4566',
                         region_name='us-east-1',
                         aws_access_key_id='anything',
                         aws_secret_access_key='anything')


def create_queue(queue_name, delay_seconds, visiblity_timeout):
    """
    Create a standard SQS queue
    """
    try:
        response = sqs.create_queue(QueueName=queue_name,
                                    Attributes={
                                        'DelaySeconds': delay_seconds,
                                        'VisibilityTimeout': visiblity_timeout
                                    })
    except Exception as e:
        logger.exception(f'Could not create SQS queue - {e}.')
        raise
    else:
        return response


def send_message(queue_name, message):
    """
    Send message to SQS queue
    """
    try:
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(MessageBody=message)
    except Exception as e:
        logger.exception(f'Could not send message to SQS queue - {e}.')
        raise
    else:
        return response


def receive_message(queue_name):
    """
    Receive message from SQS queue
    """
    try:
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.receive_messages()
    except Exception as e:
        logger.exception(f'Could not receive message from SQS queue - {e}.')
        raise
    else:
        return response


if __name__ == '__main__':
    # CONSTANTS
    QUEUE_NAME = 'queue-2'
    DELAY_SECONDS = '0'
    VISIBLITY_TIMEOUT = '60'
    connect_sqs()
    output = create_queue(QUEUE_NAME, DELAY_SECONDS, VISIBLITY_TIMEOUT)
    logger.info(
        f'Standard Queue {QUEUE_NAME} created. Queue URL - {output.url}')

    # Send message to SQS queue
    message = {
        'id': 1,
        'name': 'John Doe',
        'age': 25

    }
    message = json.dumps(message)
    output = send_message(QUEUE_NAME, message)
    logger.info(f'Message sent to SQS queue - {output.get("MessageId")}')

    # Receive message from SQS queue
    output = receive_message(QUEUE_NAME)
    output = json.loads(output[0].body)
    logger.info(f'Message received from SQS queue - {output}')
