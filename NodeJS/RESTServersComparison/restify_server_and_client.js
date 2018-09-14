var restify = require('restify');

// State
var next_user_id = 0;
var users = {};

// Server
var server = restify.createServer({
  name: 'myapp',
  version: '1.0.0'
});
server.use(restify.acceptParser(server.acceptable));
server.use(restify.queryParser());
server.use(restify.bodyParser());

function testing_more_functions2(req, res, next) {
  req.blah['b'] = 1;
  console.log("AQUI2 "+JSON.stringify(req.blah));
  next();
}

function testing_more_functions3(req, res, next) {
  req.blah['c'] = 1;
  console.log("AQUI3 "+JSON.stringify(req.blah));
}

server.get("/", function (req, res, next) {
  res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(users));
  req.blah = {}
  req.blah['a'] = 1;
  console.log("AQUI "+JSON.stringify(req.blah));
  return next();
}, testing_more_functions2, testing_more_functions3);

server.get('/user/:id', function (req, res, next) {
  res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(users[parseInt(req.params.id)]));
  return next();
});

server.post('/user', function (req, res, next) {
  var user = req.params;
  user.id = next_user_id++;
  users[user.id] = user;
  res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(user));
  return next();
});

server.put('/user/:id', function (req, res, next) {
  var user = users[parseInt(req.params.id)];
  var changes = req.params;
  delete changes.id;
  for(var x in changes) {
    user[x] = changes[x];
  }
  res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(user));
  return next();
});

server.del('/user/:id', function (req, res, next) {
  delete users[parseInt(req.params.id)];
  res.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
  res.end(JSON.stringify(true));
  return next();
});

server.listen(8000, function () {
  console.log('%s listening at %s', server.name, server.url);
});

// Client
var client = restify.createJsonClient({
  url: 'http://localhost:8000',
  version: '~1.0'
});

client.post('/user', { name: "John Doe" }, function (err, req, res, obj) {
  if(err) console.log("An error ocurred:", err);
  else console.log('POST    /user   returned: %j', obj);
  
  client.get('/user/0', function (err, req, res, obj) {
    if(err) console.log("An error ocurred:", err);
    else console.log('GET     /user/0 returned: %j', obj);
    
    client.put('/user/0', { country: "USA" }, function (err, req, res, obj) {
      if(err) console.log("An error ocurred:", err);
      else console.log('PUT     /user/0 returned: %j', obj);
      
      client.del('/user/0', function (err, req, res, obj) {
        if(err) console.log("An error ocurred:", err);
        else console.log('DELETE  /user/0 returned: %j', obj);
        
        client.get('/', function (err, req, res, obj) {
          if(err) console.log("An error ocurred:", err);
          else console.log('GET     /       returned: %j', obj);
        });
      });
    });
  });
});




// /* eslint no-param-reassign: "off" */
// 'use strict';

// const restify = require('restify');
// const ClientService = require('../../../client-service');
// const NotFoundError = require('../../../errors').db.NotFoundError;

// function clientInterceptor(req, res, next) {
//     ClientService.get(req.params.clientId)
//         .then(client => {
//             if (client.status !== 'ACTIVE') {
//                 next(new restify.NotFoundError('Client isn\'t active'));
//                 return null; // e return?
//             }

//             req.parsed.client = client;
//             next();
//             return null;
//         })
//         .catch(NotFoundError, err => next(new restify.NotFoundError(err)))
//         .catch(next);
//         // .catch(err => {
//         //     if (err.code === 'ConditionalCheckFailedException') {
//         //         return next(new restify.errors.ConflictError(`[${order.clientId}] Order ${order.id} already exists.`));
//         //     }
//         //     return next(err);
//         // });
// }

// module.exports = clientInterceptor;