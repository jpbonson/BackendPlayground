// https://www.airpair.com/node.js/posts/top-10-mistakes-node-developers-make
// https://lodash.com/docs/4.16.4

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

// isString, isObject, isEmpty, isNumber, isNaN, 
// isUndefined, isArray, isObject


console.log("\n# OBJECT\n");

var object = { 'a': [{ 'b': { 'c': 3 } }] };
 
var result = _.get(object, 'a[0].b.c');
console.log(result); // => 3

var result = _.get(object, 'a[0][b][c]');
console.log(result); // => 3
 
var result = _.get(object, ['a', '0', 'b', 'c']);
console.log(result); // => 3
 
var result = _.get(object, 'a.b.c', 'default');
console.log(result); // => 'default'

var result = _.get(object, 'a.b.c', null);
console.log(result); // => null

// _.get(channel, `config.${key}`, null)



var object = { 'a': { 'b': 2 } };
var other = _.create({ 'a': _.create({ 'b': 2 }) });
 
var result = _.has(object, 'a');
console.log(result); // => true
 
var result = _.has(object, 'a.b');
console.log(result); // => true
 
var result = _.has(object, ['a', 'b']);
console.log(result); // => true
 
var result = _.has(object, ['a', 'b', 'c']);
console.log(result); // => false
 
var result = _.has(other, 'a');
console.log(result); // => false


var object = { 'a': 1, 'b': 2, 'c': 1 };
var result = _.invert(object);
console.log(result); // => { '1': 'c', '2': 'b' }


var object = {
  'a': [{ 'b': 2 }, { 'd': 4 }], 'x': 7, z: 9
};
var other = {
  'a': [{ 'c': 3 }, { 'e': 5 }], 'y': 8, z: 19
};
var result = _.merge(object, other);
console.log(result);
// => { a: [ { b: 2, c: 3 }, { d: 4, e: 5 } ], x: 7, z: 19, y: 8 }

var object = { 'a': 1, 'b': '2', 'c': 3 };
var result = _.omit(object, ['a', 'c']);
console.log(result); // => { 'b': '2' }

var object = { 'a': 1, 'b': '2', 'c': 3 };
var result = _.pick(object, ['a', 'c']);
console.log(result); // => { 'a': 1, 'c': 3 }

var object = { 'a': 1, 'b': '2', 'c': 3 };
var result = _.pickBy(object, _.isNumber);
console.log(result); // => { 'a': 1, 'c': 3 }


var object = { 'a': [{ 'b': { 'c': 3 } }] };
_.set(object, 'a[0].b.c', 4);
console.log(object.a[0].b.c); // => 4
_.set(object, ['x', '0', 'y', 'z'], 5);
console.log(object.x[0].y.z); // => 5
console.log(object); // { a: [ { b: [Object] } ], x: [ { y: [Object] } ] }


var object = { 'a': [{ 'b': { 'c': 7 } }] };
_.unset(object, 'a[0].b.c'); // => true
console.log(object); // => { 'a': [{ 'b': {} }] };
_.unset(object, ['a', '0', 'b', 'c']); // => true
console.log(object); // => { 'a': [{ 'b': {} }] };


function Foo() {
  this.a = 1;
  this.b = 2;
}
 
Foo.prototype.c = 3;
 
var result = _.values(new Foo);
console.log(result); // => [1, 2] (iteration order is not guaranteed)
 
var result = _.values('hi');
console.log(result); // => ['h', 'i']

var result = _.values({ 'a': 1, 'b': '2', 'c': 3 });
console.log(result); // => [ 1, '2', 3 ]


console.log("\n# STRING\n");

_.camelCase('Foo Bar');
// => 'fooBar'
 
_.camelCase('--foo-bar--');
// => 'fooBar'
 
_.camelCase('__FOO_BAR__');
// => 'fooBar'


_.padStart('abc', 6);
// => '   abc'
 
_.padStart('abc', 6, '_-');
// => '_-_abc'
 
_.padStart('abc', 3);
// => 'abc'


console.log("\n# UTIL\n");

_.range(4);
// => [0, 1, 2, 3]
 
_.range(-4);
// => [0, -1, -2, -3]
 
_.range(1, 5);
// => [1, 2, 3, 4]
 
_.range(0, 20, 5);
// => [0, 5, 10, 15]
 
_.range(0, -4, -1);
// => [0, -1, -2, -3]
 
_.range(1, 4, 0);
// => [1, 1, 1]
 
_.range(0);
// => []
