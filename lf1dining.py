exports.handler = (event, context, callback) => {
    console.log("incoming event details: " + JSON.stringify(event));
    const peoplecount = event.currentIntent.slots.PeopleCount;
    const cuisine = event.currentIntent.slots.Cuisine;
    const email = event.currentIntent.slots.Email;
    const time = event.currentIntent.slots.Time;
    const city = event.currentIntent.slots.City;
    const date = event.currentIntent.slots.Date;
    const outputSessionAttributes = event.sessionAttributes || {};
    let slots = event.currentIntent.slots;
    if(city==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!validate_loc(city))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "City",
            { contentType: 'PlainText', content: 'We apologize but that is not a valid entry for city. Please make a new selection.' }));
    }
    else if(cuisine==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!validate_cuisine(cuisine))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "Cuisine",
            { contentType: 'PlainText', content: 'We dont have this cuisine. Can you choose from Chinese, American, Mexican, Korean,Japanese,Italian and French' }));
    }
    else if(peoplecount==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!validate_peoplecount(peoplecount))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "PeopleCount",
            { contentType: 'PlainText', content: 'Please enter between 1 and 19' }));
    }
    else if(date==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!isValidDate(date))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "Date",
            { contentType: 'PlainText', content: 'Invalid Date' }));
    }
    else if(time==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!validate_time(time))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "Time",
            { contentType: 'PlainText', content: 'Invalid Time. Please enter a proper time' }));
    }
    else if(email==null)
    {
        callback(null,delegate(outputSessionAttributes,slots)); 
    }
    else if(!validate_email(email))
    {
        callback(null,elicitSlot(outputSessionAttributes, event.currentIntent.name,event.currentIntent.slots, "Phone",
            { contentType: 'PlainText', content: 'Invalid Phone Number. Please enter a valid phone number' }));
    }
    callback(null,delegate(outputSessionAttributes,slots)); 
};

function delegate(sessionAttributes, slots) {
    return {
        sessionAttributes,
        dialogAction: {
            "type": 'Delegate',
            "slots": slots
        }
    };
}

function validate_time(time) {
var qwerty=time.split(":");
  var now = new Date();
	var d = new Date();
now.setHours(qwerty[0]);
now.setMinutes(qwerty[1]);
d.setHours(d.getHours()-4);
console.log(qwerty[0]+" "+qwerty[1]+" "+now+" "+d);
if (now >= d) {
    return true;
}
return false;
       }

function isValidDate(dateString) {
  var varDate = new Date(dateString);
  varDate.setDate(varDate.getDate()+1);
var today = new Date();
if(varDate.getTime() >= today.getTime()) {
return true;
}
return false;
}

function validate_loc(loc){
    return loc.toLowerCase() == "manhattan"
}

function validate_peoplecount(count){
      return !isNaN(count) && count>0 && count<20;  
}

function validate_cuisine(cuisine)
{
    cuisine=cuisine.toLowerCase();
    const cuisinetypes = ['chinese', 'american', 'mexican','korean','japanese','italian','french', 'indian']
    for(let i=0;i<cuisinetypes.length;i++)
    {
        if(cuisinetypes[i]==cuisine)
            return true;
    }
    return false;
}

function validate_email(inputtxt) {
  return true;
}

function elicitSlot(sessionAttributes, intentName, slots, slotToElicit, message) {
     return {
        sessionAttributes,
        dialogAction: {
            type: 'ElicitSlot',
            intentName,
            slots,
            slotToElicit,
            message,
         
        },
    };
}

