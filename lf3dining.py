import boto3
import json
import requests
import random
import json
from requests_aws4auth import AWS4Auth

region = 'us-east-1' 
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
dynamo = boto3.client('dynamodb', region_name='us-east-1')
host = 'https://search-search-qwd3x3xfvps2llb4wwmiibd66q.us-east-1.es.amazonaws.com'
index = 'restaurants'
url = host + '/' + index + '/_search'
ses_client = boto3.client("ses", region_name="us-east-1")
def lambda_handler(event, context):
    print(event)
    print(context)
    for record1 in event["Records"]:
        record=json.loads(record1["body"])
        query = { "query": { "term":{ "category.S": record["Cuisine"] }}, "fields": ["_id"], "_source": False}
        print(query)
        headers = { "Content-Type": "application/json" }
        r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
        r=r.json()
        print(r)
        length=len(r["hits"]["hits"])
        print(length)
        option1, option2, option3 = random.sample(range(0,length-1), 3)
        one=r["hits"]["hits"][option1]
        two=r["hits"]["hits"][option2]
        three=r["hits"]["hits"][option3]
        data1 = dynamo.get_item( TableName='yelp-restaurants', Key={ 'id': { 'S': one["_id"] }})
        data2 = dynamo.get_item( TableName='yelp-restaurants', Key={ 'id': { 'S': two["_id"] }})
        data3 = dynamo.get_item( TableName='yelp-restaurants', Key={ 'id': { 'S': three["_id"] }})
        print(data1["Item"]['name'])
        result = "Hello! Here are my "+record["Cuisine"]+" restaurant suggestions for "+record["PeopleCount"]+" people, for "+record["Date"]+" at "+record["Time"]+" : 1."+data1["Item"]['name']['S']+",located at "+data1["Item"]['address']['S']+", 2."+data2["Item"]['name']['S']+",located at "+data2["Item"]['address']['S']+", 3."+data3["Item"]['name']['S']+",located at "+data3["Item"]['address']['S']+". Enjoy your meal!”"
        print(result)
        CHARSET = "UTF-8"
        response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                record["Email"],
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": result,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Restaurant Suggestion" ,
            },
        },
        Source=record["Email"],
    )
        
        print(response)
    return response