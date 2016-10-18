// https://strongloop.com/strongblog/compare-express-restify-hapi-loopback/

var express = require('express');
var Item = require('models').Item;

var app = express();
var itemRoute = express.Router();
 
itemRoute.param('itemId', function(req, res, next, id) {
  Item.findById(req.params.itemId, function(err, item) {
    req.item = item;
    next();
  });
});
 
// Create new Items
itemRoute.post('/', function(req, res, next) {
  var item = new Item(req.body);
  item.save(function(err, item) {
    res.json(item);
  });
});
 
itemRoute.route('/:itemId')
  // Get Item by Id
  .get(function(req, res, next) {
    res.json(req.item);
  })
  // Update an Item with a given Id
  .put(function(req, res, next) {
    req.item.set(req.body);
    req.item.save(function(err, item) {
      res.json(item);
    });
  })
  // Delete and Item by Id
  .delete(function(req, res, next) {
    req.item.remove(function(err) {
      res.json({});
    });
  });
 
app.use('/api/items', itemRoute);
app.listen(8080);