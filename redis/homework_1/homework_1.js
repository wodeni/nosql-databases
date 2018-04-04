var request  = require('request');

var base_url = 'https://api.nasa.gov/planetary/apod';
var api_key  = 'api_key=ZlBh4nuLRSvjxeNUyRYDqtDw5BGfmaV3BWukfi8q';
var date     = 'date=2017-09-17'
var query    = base_url + '?' + api_key + '&' + date;

request(query, { json: true }, (err, res, body) => {
    if (err)  
        return console.log(err); 
    console.log(body.url);
});

