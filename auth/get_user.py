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
    
    # TODO - need to validate the parameters and results before proceeding further 

    print("Get the details of the User basing on the given phone number")

    statusCode = 400
    print(event['pathParameters'])
    if event['pathParameters']['phone_number']:
        filtering_exp = Key('phone_number').eq(event['pathParameters']['phone_number'])
        statusCode = 200
        result = table.scan(FilterExpression=filtering_exp)
    else:
        print("A")
        result = {
            "error":"No user with {} found".format(event['pathParameters']['phone_number'])
        }

    print("B")
    # create a response
    response = {
        "statusCode": statusCode,
        "body": json.dumps(result['Items'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
