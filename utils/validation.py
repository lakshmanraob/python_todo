import json
import logging
import os
import time
import uuid

import boto3
from todos import decimalencoder
dynamodb = boto3.resource('dynamodb')
from todos import constants

def is_valid_request(event):

    headers = event['headers']

    if 'Authorization' in headers:
        access_token = headers['Authorization'].split(' ')
        if len(access_token) > 1:
            return True

    return False

def get_access_token(event):

    headers = event['headers']

    if 'Authorization' in headers:
        access_token = headers['Authorization'].split(' ')
        if len(access_token) > 1:
            return access_token[1]

    return ''