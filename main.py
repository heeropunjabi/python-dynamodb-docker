#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Heero"
__version__ = "0.0.1"
__license__ = "MIT"

from logzero import logger
import boto3

dynamodb = None


def connect_dynamodb():
    global dynamodb
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url='http://localhost:4566',
                              region_name='us-east-1',
                              aws_access_key_id='anything',
                              aws_secret_access_key='anything')


def create_table(tbl_name):
    table = dynamodb.create_table(
        TableName=tbl_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition Key Only
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=tbl_name)
    print(table.item_count)
    print(table.creation_date_time)
    print(table.table_status)
    print(table.table_name)


def insert_data(tbl_name, **item):
    table = dynamodb.Table(tbl_name)
    table.put_item(
        Item=item,
    )


def get_data(tbl_name, **item):
    table = dynamodb.Table(tbl_name)
    response = table.get_item(
        Key=item,
    )
    return response['Item']


def main():
    """ Main entry point of the app """
    logger.info("Start")
    tbl_name = 'test3'
    connect_dynamodb()
    create_table(tbl_name)
    insert_data(tbl_name, id=1, name='Heero')
    print(get_data(tbl_name, id=1))
    logger.info("End")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
