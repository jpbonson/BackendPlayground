// sudo apt install mongodb-server
// curl -i -X POST -H 'Content-Type: application/json' -d '{'title':'test' , 'description':'x' , 'location':'y'}' http://127.0.0.1:8080/jobs
// curl -is http://127.0.0.1:8080/jobs

var restify = require('restify');

var routes = require('./routes');
var env = require('./env');

var server = restify.createServer({
    name : process.env.app_name
});

server.use(restify.queryParser());
server.use(restify.bodyParser());

server.get('/jobs', routes.findAllJobs);
server.get('/jobs/:jobId', routes.findJob);
server.post('/jobs', routes.postNewJob);
server.del('/jobs/:jobId', routes.deleteJob);

 server.listen(process.env.port, process.env.ip_addr, function(){
    console.log('%s listening at %s ', server.name , server.url);
});