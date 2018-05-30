import os

class constants:
    DYNAMO_DB_TABLE_NAME = os.environ['DYNAMODB_TABLE']
    USER_DB_TABLE_NAME = os.environ['USER_TABLE']
    ITEMS_DB_TABLE = os.environ['ITEM_TABLE']
    OUTLET_DB_TABLE = os.environ['OUTLET_TABLE']
    ORDER_DB_TABLE = os.environ['ORDER_TABLE']