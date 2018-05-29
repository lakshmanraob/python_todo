import json
import logging
import os
import time
import uuid

import boto3
from todos import decimalencoder
dynamodb = boto3.resource('dynamodb')
from todos import constants
from utils import validation

'''

    for adding the new outlets use this method

'''
# creating the OutLet by accepting the OutLet model
def create_outlet(event,context):
    data = json.loads(event['body'])
    headers = event['headers']
    
    print(headers['Authorization'])

    if validation.is_valid_request(event):
        auth_token = validation.get_access_token(event)

        if not auth_token:
            logging.error("Auth token missing")
            return create_error_response(400,'Auth token missing')
    else:
        return create_error_response(400,'Auth token missing')

    if 'name' not in data:
        logging.error("Name Validation Failed")
        return create_error_response(400,'name missing')
    elif 'lat' not in data:
        logging.error("Lattitude Validation Failed")
        return create_error_response(401,'lattitude is missing')
    elif 'lng' not in data:
        logging.error("Longitude Validation Failed")
        return create_error_response(401,'Longitude is missing')
    
    create_timestamp = int(time.time() * 1000)

    outlet_table = dynamodb.Table(constants.constants.OUTLET_DB_TABLE)

    outlet_item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'lat': data['lat'],
        'lng': data['lng'],
        'createdBy': validation.get_access_token(event),
        'createdAt': create_timestamp,
        'updatedAt': create_timestamp
    }

    # adding the categories for the outlet
    if data['categories']:
        outlet_item['categories'] = []
        for category in data['categories']:
            category['id'] = str(uuid.uuid1())
            outlet_item['categories'].append(category)

    # write the Outlet to the database
    outlet_table.put_item(Item=outlet_item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(outlet_item)
    }

    return response

# create a endpoint for adding categories to the outlets
# outlets/{outlet_id} - POST with categories model in the body

def create_categories(event, context):
    data = json.loads(event['body'])
    if validation.is_valid_request(event):
        auth_token = validation.get_access_token(event)

        if not auth_token:
            logging.error("Auth token missing")
            return create_error_response(400,'Auth token missing')
    else:
        return create_error_response(400,'Auth token missing')

    outlet_table = dynamodb.Table(constants.constants.OUTLET_DB_TABLE)

    # fetch todo from the database
    result = outlet_table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # update the table and return the new item - that is the logic

    items_json = result['Item']

    if items_json:
        if items_json['categories']:
            for category in data['categories']:
                category['id'] = str(uuid.uuid1())
                items_json['categories'].append(category)
        else:
            items_json['categories'] = data['categories']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(items_json,
                           cls=decimalencoder.DecimalEncoder)
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