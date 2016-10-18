// http://www.bryanbraun.com/2014/11/27/every-possible-way-to-define-a-javascript-function
// http://davidbcalhoun.com/2011/different-ways-of-defining-functions-in-javascript-this-is-madness/
// https://www.nczonline.net/blog/2013/09/10/understanding-ecmascript-6-arrow-functions/


//// Function Declarations

// Named Function Declaration
// - Functions declared like this are "hoisted", meaning, the 
// javascript engine reads all these declarations first before 
// executing any of the rest of the code. The declaration statement 
// stands alone, and cannot be combined with other expressions.

function sum(num1,num2){
  return num1 + num2;
}


//// Function Expressions (can be Named or Anonymous, except the arrow one)

// Variable Assignment
// - this variation is NOT hoisted

var sum = function(num1, num2){
  return num1 + num2;
};

// Immediately invoked
// - This function is immediately invoked, meaning that it is 
// defined and called at the same time.

(function(num1, num2){
  return num1 + num2;
}(1, 2));

// Property Assignment
// - By assigning functions (either named or unnamed) to properties of
// objects, we define methods on those objects. We can also use this
// to namespace our functions, and keep them out of the global scope.

var obj = {
  sum: function add(num1, num2) {
    return num1 + num2
  }
};

// Passed as Argument

setTimeout(function(){
  console.log(1 + 3);
}, 500);

// Returned (closure)

function counter() {
    var count = 0;
    return function() {
        console.log(count++);
    }
}

// Arrow Functions
// - part of the ES6 specification

// Anonymous
var sum = (num1, num2) => {return num1 + num2};

// Anonymous w/out optional bracketed return
var sum = (num1, num2) => num1 + num2;

// equivalent
var sum = function(num1, num2) {
  return num1 + num2;
};

// no parameters
var test = () => {return 999};

// returning object
var getTempItem = id => ({ id: id, name: "Temp" });
// effectively equivalent to:
var getTempItem = function(id) {

    return {
        id: id,
        name: "Temp"
    };
};

values = [1,2,3,4]
var result = values.sort(function(a, b) {
    return a - b;
});
// effectively equivalent to:
var result = values.sort((a, b) => a - b);


//// Function Constructor
// - bad performance, don't use any of them

// Function Constructor
var sum = new Function('num1', 'num2', 'return num1 + num2');

// Constructor w/apply()
var sum = Function.apply(this, ['num1', 'num2', 'return num1 + num2']);

// Immediately Invoked Constructor w/apply()
Function.apply(this, ['num1', 'num2', 'return num1 + num2']).apply(this, [1,2]);


// 

console.log(sum(1,1));
console.log(obj.sum(1, 2));

var bob = {}, rob = {};
bob.count = counter();
rob.count = counter();
bob.count(); // alerts "0"
bob.count(); // alerts "1"
rob.count(); // alerts "0"
rob.count(); // alerts "1"

console.log(test());


// More examples
function A(){};             // function declaration
var B = function(){};       // function expression
var C = (function(){});     // function expression with grouping operators
var D = function foo(){};   // named function expression
var E = (function(){        // IIFE that returns a function
  return function(){}
})();
var F = new Function();     // Function constructor
var G = new function(){};   // special case: object constructor
var H = x => x * 2;         // ES6 arrow function

console.log(H(7))
