import json
def lambda_handler(event, context):
    # TODO implement
    message_string = {
            "messages": [
                {
                    "type": "unstructured",
                    "unstructured": {
                        "id": "string",
                        "text": "Application under development. Search functionality will be implemented in Assignment 2",
                        "timestamp": "string"
                    }
                }
            ]
        }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(message_string)
    }