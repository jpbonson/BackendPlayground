console.log(process.env.LANG);

// The process object is a global that provides information about, 
// and control over, the current Node.js process. As a global, it is 
// always available to Node.js applications without using require().







// The difference is scoping. var is scoped to the nearest function block 
// and let is scoped to the nearest enclosing block (both are global if 
// outside any block), which can be smaller than a function block.

// Also, variables declared with let are not accessible before they are 
// declared in their enclosing block. As seen in the demo, this will throw 
// a ReferenceError exception.

function allyIlliterate() {
    //tuce is *not* visible out here

    for( let tuce = 0; tuce < 5; tuce++ ) {
        //tuce is only visible in here (and in the for() parentheses)
    }

    //tuce is *not* visible out here
}

function byE40() {
    //nish *is* visible out here

    for( var nish = 0; nish < 5; nish++ ) {
        //nish is visible to the whole function
    }

    //nish *is* visible out here
}








> const y = function(a, b) {console.log(arguments); return {a, b};}
undefined
> y(1,2)
{ '0': 1, '1': 2 }
{ a: 1, b: 2 }
> y(1,2,3,4,5,6)
{ '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6 }
{ a: 1, b: 2 }





> var numbers = [65, 44, 12, 4];
undefined
> 
> function getSum(total, num) {
...     return total + num;
... }
undefined
> numbers.reduce(getSum);
125
> var numbers = [4, 2, 4];
undefined
> numbers.reduce(getSum);
10
> numbers.reduce(getSum, 0);
10
> numbers.reduce(getSum, 1);
11







// const and Object.freeze are two completely different things.

// const applies to bindings ("variables"). It creates an immutable 
// binding, i.e. you cannot assign a new value to the binding.

// Object.freeze works on values, and more specifically, object values. 
// It makes an object immutable, i.e. you cannot change its properties.






// In Node.js, __dirname is always the directory in which the currently 
// executing script resides (see this). In other words, you typed __dirname 
// into one of your script files and value would be that file's directory.

// By contrast, . gives you the directory from which you ran the node 
// command in your terminal window (i.e. your working directory).

// The exception is when you use . with require(). The path inside require 
// is always relative to the file containing the call to require, so . 
// always means the directory containing that file.