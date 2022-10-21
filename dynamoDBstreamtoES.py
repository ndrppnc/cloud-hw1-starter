import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1' # e.g. us-east
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-search-qwd3x3xfvps2llb4wwmiibd66q.us-east-1.es.amazonaws.com' # the OpenSearch Service domain, with https://
index = 'restaurants'
type = 'restaurant'
url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):
    count = 0
    for record in event['Records']:
        # Get the primary key for use as the OpenSearch ID
        id = record['dynamodb']['Keys']['id']['S']

        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id, auth=awsauth)
        else:
            document = record['dynamodb']['NewImage']
            r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
            print(r.content,document,url+id,awsauth)
        count += 1
    print("success")
    return str(count) + ' records processed.'