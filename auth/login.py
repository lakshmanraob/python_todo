import json
import logging
import os
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key, Attr
from todos import decimalencoder
dynamodb = boto3.resource('dynamodb')
from todos import constants

# creating the user by accepting the user model
def login(event,context):
    user_table = dynamodb.Table(constants.constants.USER_DB_TABLE_NAME)

    # access the phone_number and pin. And validate against the db values
    statusCode = 400
    payload = json.loads(event['body'])

    if event['body']:
        # filte_phone_exp = Key('phone_number').eq(payload['phone_number'])
        # filter_pin_exp = Key('pin').eq(payload['pin'])
        statusCode = 200
        # result = user_table.scan(FilterExpression=(filte_phone_exp and filter_pin_exp))
        result = user_table.scan(
              Select= 'ALL_ATTRIBUTES',
              FilterExpression=Attr('phone_number').eq(payload['phone_number']) & Attr('pin').eq(payload['pin']) 
              )
    else:
        print("A")
        result = {
            "error":"No user with {} found".format(payload['phone_number'])
        }

    # create a response
    response = {
        "statusCode": statusCode,
        "headers": {
            'Access-token': '{}'.format(result['Items'][0]['id'])
        },
        "body": json.dumps(result['Items'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response