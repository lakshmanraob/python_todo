import json
import logging
import os
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key, Attr
from todos import decimalencoder, constants
from utils import validation, helper

dynamodb = boto3.resource('dynamodb')

# creating the user by accepting the user model
'''
    this method to handle the orders against the availbale categories
'''
def item_request(event,context):
    if validation.is_valid_request(event):
        auth_token = validation.get_access_token(event)

        if not auth_token:
            logging.error("Auth token missing")
            return helper.create_error_response(400,'Auth token missing')
    else:
        return helper.create_error_response(400,'Auth token missing')

    category_table = dynamodb.Table(constants.constants.ITEMS_DB_TABLE)
    order_table = dynamodb.Table(constants.constants.ORDER_DB_TABLE)

    order_timestamp = int(time.time() * 1000)

    print(event['body'])
    data = json.loads(event['body'])
    category_id = data['category_id']
    quantity = data['request_content']

    if category_id:
         # fetch todo from the database
        result = category_table.get_item(
            Key={
                'id': category_id
            }
        )

         # update the table and return the new item - that is the logic
        if 'Item' in result:
            categories_json = result['Item']
            print(categories_json)
        else:
            print("no item aviable")
            return helper.create_error_response(400,'Unable to serve you at this point of time')
        
        if len(categories_json) > 0:
            if categories_json['available'] >= quantity:
                remaining = categories_json['available'] - quantity
                order_item = {
                    "id":str(uuid.uuid1()),
                    "createdAt":order_timestamp,
                    "category_id":category_id,
                    "request_content":data['request_content'],
                    "orderedBy":validation.get_access_token(event)
                }
                
                # updating the category table
                update_result = category_table.update_item(
                    Key={
                        'id': data['category_id']
                    },
                    ExpressionAttributeValues={
                        ':available': remaining,
                        ':updatedAt': order_timestamp,
                    },
                    UpdateExpression='SET '
                         'available = :available, '
                         'updatedAt = :updatedAt',
                    ReturnValues='ALL_NEW',
                )

                print("update result ",update_result)
                order_table.put_item(Item=order_item)
                print("update the category with transaction")

                # create a response
                response = {
                    "statusCode": 200,
                    "body": json.dumps(update_result['Attributes'],
                               cls=decimalencoder.DecimalEncoder)
                }
                return response
            else:
                response =  helper.create_error_response(400,'Unable to serve you at this point of time')
                return response
        else:
            return helper.create_error_response(400,'Unable to find the category')
    else:
        return helper.create_error_response(400,'Unable to find the category')