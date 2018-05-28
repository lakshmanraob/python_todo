import os

class constants:
    DYNAMO_DB_TABLE_NAME = os.environ['DYNAMODB_TABLE']
    USER_DB_TABLE_NAME = os.environ['USER_TABLE']