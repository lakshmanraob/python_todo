import json
import logging
import os
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key, Attr
from todos import decimalencoder, constants
from utils import validation

dynamodb = boto3.resource('dynamodb')

# creating the user by accepting the user model
def item_request(event,context):
    items_table = dynamodb.Table(constants.constants.ITEMS_DB_TABLE)

    # access the phone_number and pin. And validate against the db values
    statusCode = 400
    payload = json.loads(event['body'])

    text = "invalid access_token"
    if validation.is_valid_request(event=event):
        auth_key = validation.get_access_token(event=event)
        if auth_key:
            statusCode = 200
            text = "ok"
    else:
        text = "invalid key" 

    # create a response
    response = {
        "statusCode": statusCode,
        "body": json.dumps(text)
    }
    return response