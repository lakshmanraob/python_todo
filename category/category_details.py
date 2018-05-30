import json
import logging
import os

from todos import decimalencoder
from todos import constants
from utils import validation, helper
import boto3
dynamodb = boto3.resource('dynamodb')


def category_list(event):
    table = dynamodb.Table(constants.constants.OUTLET_DB_TABLE)

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response

'''
    getting the category details, send the category Id for getting the details
'''

def get_category_details(event, context):

    if validation.is_valid_request(event):
        auth_token = validation.get_access_token(event)

        if not auth_token:
            logging.error("Auth token missing")
            return helper.create_error_response(400,'Auth token missing')
    else:
        return helper.create_error_response(400,'Auth token missing')

    category_table = dynamodb.Table(constants.constants.ITEMS_DB_TABLE)

    category_id = event['pathParameters']['id']

    if category_id:
         # fetch todo from the database
        result = category_table.get_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )

         # update the table and return the new item - that is the logic
        category_json = result['Item']

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(category_json,
                           cls=decimalencoder.DecimalEncoder)
        }
        return response
    else:
        return helper.create_error_response(400,'Auth token missing')