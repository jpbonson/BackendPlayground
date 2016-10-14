'use strict';

const _ = require('lodash');

console.log("Testing lodash library...\n");


console.log("\n# ARRAYS\n");

var result = _.difference([2, 1, 3, 5], [2, 3, 4]);
console.log(result); // => [ 1, 5 ]

var result = _.union([2], [1, 2], [3,1,1,4]);
console.log(result); // => [ 2, 1, 3, 4 ]


console.log("\n# COLLECTIONS (Array|Object|string)\n");

_.forEach([1, 2], function(value) {
  console.log(value); // => Logs `1` then `2`.
});
 
_.forEach({ 'a': 1, 'b': 2 }, function(value, key) {
  console.log(value+':'+key); // => Logs '1:a' then '2:b' (iteration order is not guaranteed).
});



// The includes (formerly called contains and include) method compares objects by reference 
// (or more precisely, with ===). Because the two object literals of {"b": 2} in your example 
// represent different instances, they are not equal. Notice:
// 
// ({"b": 2} === {"b": 2})
// > false
// 
// However, this will work because there is only one instance of {"b": 2}:
// 
// var a = {"a": 1}, b = {"b": 2};
// _.includes([a, b], b);
// > true
// 
// On the other hand, the where and find methods compare objects by their properties, so they 
// don't require reference equality. As an alternative to includes, you might want to try some 
// (also aliased as any):
// 
// _.some([{"a": 1}, {"b": 2}], {"b": 2})
// > true


var result = _.includes([1, 2, 3], 1);
console.log(result); // => true
 
var result = _.includes([1, 2, 3], 1, 2);
console.log(result); // => false

var result = _.includes([[1, 2], 3], [1, 2]);
console.log(result); // => false

var x = [1, 2]
var result = _.includes([x, 3], x);
console.log(result); // => true
 
var result = _.includes({ 'a': 1, 'b': 2 }, 1);
console.log(result); // => true

var result = _.includes({ 'a': 1, 'b': 2 }, 'a');
console.log(result); // => false
 
var result = _.includes('abcd', 'bc');
console.log(result); // => true

var users = [
  { 'user': 'fred',   'age': 48 },
  { 'user': 'barney', 'age': 46 },
  { 'user': 'fred',   'age': 40 },
  { 'user': 'barney', 'age': 34 }
];
 
var result = _.sortBy(users, [function(o) { return o.user; }]);
console.log(result);
//[ { user: 'barney', age: 46 },
//  { user: 'barney', age: 34 },
//  { user: 'fred', age: 48 },
//  { user: 'fred', age: 40 } ]
 
var result = _.sortBy(users, ['user', 'age']);
console.log(result);
//[ { user: 'barney', age: 34 },
//  { user: 'barney', age: 46 },
//  { user: 'fred', age: 40 },
//  { user: 'fred', age: 48 } ]

var result = _.sortBy(users, ['age']);
console.log(result);
//[ { user: 'barney', age: 34 },
//  { user: 'fred', age: 40 },
//  { user: 'barney', age: 46 },
//  { user: 'fred', age: 48 } ]


console.log("\n# LANG\n");

var objects = [{ 'a': 1 }, { 'b': 2 }];
 
var shallow = _.clone(objects);
console.log(shallow[0] === objects[0]); // => true

var deep = _.cloneDeep(objects);
console.log(deep[0] === objects[0]); // => false

var object = { 'a': 1 };
var other = { 'a': 1 };
 
var result = _.isEqual(object, other);
console.log(result); // => true
 
var result = object === other;
console.log(result); // => false

var result = object == other;
console.log(result); // => false


// _.omit(res.body, keys);
// _.range(2, totalPages + 1)
// _.get(channel, `config.${key}`, null)
// _.pick(fixtures.order(), 'hubId');
// _.pickBy(object, value => !_.isNull(value) && value !== '' && !_.isUndefined(value));
// _.padStart(index, 2, '0');
// _.isString(value)
// _.isObject(value)
// _.isEmpty(customer.CustomerName)
// _.has(customer, 'Contact.ContactAddresses')
// _.isNumber(order.OrderId)
// _.isNaN(stock.Quantity)
// _.isUndefined(order.hubId)
// _.isArray(price.prices)
// _.values(converted[key]);
// _.invert(toMagento)
// _.isObject(object)
// _.unset(customer, 'connectorStatus')
// _.set(newAddresses, `${addressKey}.status`, 'INACTIVE');
// _.camelCase(entity)
// 
// _.merge(sku, {
//     basePrice: value.parent_item.original_price,
//     discount: value.parent_item.discount_amount,
//     price: value.parent_item.price
// });