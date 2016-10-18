// sudo apt install mongodb-server
// curl -i -X POST -H 'Content-Type: application/json' -d '{'title':'test' , 'description':'x' , 'location':'y'}' http://127.0.0.1:8080/jobs
// curl -is http://127.0.0.1:8080/jobs

var express = require('express');
var bodyParser = require('body-parser')

var routes = require('./routes');
var env = require('./env');

var app = express({
    name : process.env.app_name
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

app.get('/jobs', routes.findAllJobs);
app.get('/jobs/:jobId', routes.findJob);
app.post('/jobs', routes.postNewJob);
app.delete('/jobs/:jobId', routes.deleteJob);

// app.listen(process.env.port, process.env.ip_addr, function(){
//     console.log('%s listening at %s ', app.name , app.url);
// });

app.listen(process.env.port, function() {
  console.log('listening on '+process.env.port)
})