import json

def create_error_response(status_code=400,status_string='status_string'):
    error = {
        "error_txt": status_string
    }

    # create a response
    response = {
        "statusCode": status_code,
        "body": json.dumps(error)
    }

    print("from method",response)
    return response