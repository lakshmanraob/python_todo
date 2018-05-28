import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')
from todos import constants

# creating the user by accepting the user model
def create_user(event,context):
    data = json.loads(event['body'])
    if 'phone_number' not in data:
        logging.error("phone number Validation Failed")
        # raise Exception("Couldn't create the user item, phone number missing")
        return create_error_response(400,'phone number missing')
    elif 'pin' not in data:
        logging.error("pin Validation Failed")
        # raise Exception("Couldn't create the user item, phone number missing")
        return create_error_response(401,'pin is missing')
    
    user_timestamp = int(time.time() * 1000)

    user_table = dynamodb.Table(constants.constants.USER_DB_TABLE_NAME)

    user_item = {
        'id': str(uuid.uuid1()),
        'phone_number': data['phone_number'],
        'pin': data['pin'],
        'createdAt': user_timestamp,
        'updatedAt': user_timestamp
    }

    # write the todo to the database
    user_table.put_item(Item=user_item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(user_item)
    }

    return response

def create_error_response(status_code=400,status_string='status_string'):
    error = {
        'error_txt': status_string
    }

    # create a response
    response = {
        "status_code": status_code,
        "body": json.dumps(error)
    }

    return response