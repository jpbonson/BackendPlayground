var restify = require('restify');

var server = restify.createServer();

server.get('/hello/:name', function(req, res) {
    res.send('hello ' + req.params.name);
});

server.listen(3000, function() {
    console.log('Listening on port 3000');
});