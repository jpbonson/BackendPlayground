// pm2 kill
// 
// pm2 start pm2.json
// ou
// PM2_GRACEFUL_TIMEOUT=5000 pm2 start pm2.json
// 
// pm2 gracefulReload pm2.json

'use strict';

const restify = require('restify');

function respond(req, res, next) {
    setTimeout(() => {
        res.send('hello');
        next();
    }, 30000);
}

var server = restify.createServer();

server.get('/hello', respond);

server.listen(8080, function() {
  console.log('%s listening at %s', server.name, server.url);
});


process.on('message', message => {
    if (message === 'shutdown') {
        console.log('message shutdown');
        server.close(() => {
            console.log('all connections were successfully handled');
            process.exit(0);
        });
    }
});
