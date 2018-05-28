import os
import json

from todos import constants
from todos import decimalencoder
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')

def user_details(event, context):
    table = dynamodb.Table(constants.constants.USER_DB_TABLE_NAME)

    # # fetch user details from the database
    # result = table.get_item(
    #     Key={
    #         'phone_number': event['pathParameters']['phone_number']
    #     }
    # )

    # print("Movies from 1992 - titles A-L, with genres and lead actor")
    print("Get the details of the User bassing on the given phone number")

    statusCode = 400
    if event['pathParameters']['phone_number']:
        filtering_exp = Key('phone_number').eq(event['pathParameters']['phone_number'])
        statusCode = 200
        result = table.scan(FilterExpression=filtering_exp)
    else:
        result = {
            "error":"No user with {} found".format(event['pathParameters']['phone_number'])
        }

    # create a response
    response = {
        "statusCode": statusCode,
        "body": json.dumps(result['Items'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
