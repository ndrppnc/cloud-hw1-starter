import json
import boto3
client = boto3.client('lex-runtime')
def lambda_handler(event, context):
    usertext=event["messages"][0]["unstructured"]["text"]
    response = client.post_text(
    botName='diningbot',
    botAlias='diningbot',
    userId='1234567890',
    sessionAttributes={
    },
    requestAttributes={
    },
    inputText=usertext,
    activeContexts=[
    ]
)
    print(response["message"])
    return {
        'statusCode': 200,
        'messages': [{'type': 'unstructured', 'unstructured': {'text': response["message"]}}]
    }