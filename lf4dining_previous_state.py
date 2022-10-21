var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});
exports.handler = (event, context, callback) => {
    var user="1234567890"
    const outputSessionAttributes = event.sessionAttributes || {};
    var params = {TableName: 'conciergestate',Key:{"userID":{"S":user}}};
    console.log(params);
    ddb.getItem(params, function(err, data) {
    if (err) {
    callback(null,close(outputSessionAttributes,'Fulfilled',{'contentType': 'PlainText',
                  'content': "You didn't make any previous search"})); 
    } else {
        params=data.Item.search.M;
    console.log("Success", data.Item.search.M);
    var params2={PeopleCount:params.PeopleCount.S, Cuisine:params.Cuisine.S, Time:params.Time.S, City:params.City.S, Phone:params.Phone.S, Date:params.Date.S};
    console.log(params2);
    var params1 = {
  MessageBody: JSON.stringify(params2),
  QueueUrl: "https://sqs.us-east-1.amazonaws.com/838023884170/diningmessage.fifo",
  MessageGroupId: "diningsuggestions"
    };
    sqs.sendMessage(params1, function(err, data) {
     if (err) {
    console.log("Error", err);
    } else {
    console.log("Success", data.MessageId);
   }
   });
    callback(null,close(outputSessionAttributes,'Fulfilled',{'contentType': 'PlainText',
                  'content': "You’re all set. Expect my suggestions shortly! Have a good day."})); 
  }
});

   return "fdv";
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