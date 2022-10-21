var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});
var docClient = new AWS.DynamoDB.DocumentClient();
exports.handler = (event, context, callback) => {
    const outputSessionAttributes = event.sessionAttributes || {};
    callback(null,close(outputSessionAttributes,'Fulfilled',{'contentType': 'PlainText',
                  'content': "You’re all set. Expect my suggestions shortly! Have a good day."})); 
    var pastsearch = {
  TableName: 'conciergestate',
  Item: {
    'userID' : '1234567890',
    'search': event.currentIntent.slots
  }
};
docClient.put(pastsearch, function(err, data) {
  if (err) console.log(err);
  else console.log(data);
});
    var params = {
  MessageBody: JSON.stringify(event.currentIntent.slots),
  QueueUrl: "https://sqs.us-east-1.amazonaws.com/************/diningmessage.fifo",
  MessageGroupId: "diningsuggestions"
    };
    sqs.sendMessage(params, function(err, data) {
     if (err) {
    console.log("Error", err);
    } else {
    console.log("Success", data.MessageId);
   }
   });
}

function close(session_attributes, fulfillment_state, message) {
     return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
}
