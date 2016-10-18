var express = require('express');

var app = express();

app.get('/hello/:name', function(req, res){
    res.send('hello ' + req.params.name);
});

app.listen(3000, function() {
    console.log('Listening on port 3000');
});