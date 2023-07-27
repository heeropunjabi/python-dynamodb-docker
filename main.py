#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Heero"
__version__ = "0.0.1"
__license__ = "MIT"

from logzero import logger
import boto3
from datetime import datetime, timedelta
import simplejson as json
dynamodb = None


def connect_dynamodb():
    # boto3.Cognito.IdentityProvider().admin_reset_user_password(
    #     UserPoolId='us-east-1_0X0X0X0X0',
    #     Username='test',
    # )
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

def delete_table(tbl_name):
    table = dynamodb.Table(tbl_name)
    table.delete()
    table.meta.client.get_waiter('table_not_exists').wait(TableName=tbl_name)    


def insert_data(tbl_name, **item):
    table = dynamodb.Table(tbl_name)
    

    table.put_item(
        Item=item
    )

def update_data(tbl_name, **item):
    table = dynamodb.Table(tbl_name)
    
    table.update_item(
        Key={
            'id': item['id']
        },
        UpdateExpression="set age=:c,surname=:n, created_at=:d",
        ExpressionAttributeValues={
            ':c': item['age'],
            ':n': item['surname'],
            ':d': datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        },
        ReturnValues="UPDATED_NEW"
    )
    print("UpdateItem succeeded:")
    # print(response)


def get_data(tbl_name, **item):
    table = dynamodb.Table(tbl_name)
    
        
    response = table.get_item(
        Key=item,
    )
    print("GetItem succeeded:")
    if 'Item' not in response: 
        print("No data found")
        return
    return response['Item']


def items_length(tbl_name):
    table = dynamodb.Table(tbl_name)
    return table.item_count


def main():
    """ Main entry point of the app """
    logger.info("Start")
    tbl_name = 'test'
    connect_dynamodb()
    delete_table(tbl_name)
    create_table(tbl_name)
    insert_data(tbl_name, id=1, name='Heero')
    
    update_data(tbl_name, id=1, age=30, surname='punjabi')
    print(get_data(tbl_name, id=1))
    
    

    logger.info("End")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
