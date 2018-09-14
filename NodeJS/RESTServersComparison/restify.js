// https://strongloop.com/strongblog/compare-express-restify-hapi-loopback/
    
var restify = require('restify');
var Item = require('models').Item;

var server = restify.createServer()
 
server.use(function(req, res, next) {
  if (req.params.itemId) {
    Item.findById(req.params.itemId, function(err, item) {
      req.item = item;
      next();
    });
  }
  else {
    next();
  }
});
 
server.get('/api/items/:itemId', function(req, res, next) {
  res.send(200, req.item);
});
 
server.put('/api/items/:itemId', function(req, res, next) {
  req.item.set(req.body);
  req.item.save(function(err, item) {
    res.send(204, item);
  });
});
 
server.post('/api/items', function(req, res, next) {
  var item = new Item(req.body);
  item.save(function(err, item) {
    res.send(201, item);
  });
});
 
server.delete('/api/items/:itemId', function(req, res, next) {
  req.item.remove(function(err) {
    res.send(204, {});
  });
});
 
server.listen(8080);