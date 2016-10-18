// Remember that (despite the article's title) there's no such thing 
// as a class in JavaScript (only objects and prototypes).


// 1. Using a function

function Apple (type) {
    this.type = type;
    this.color = "red";
    this.getInfo = function() {
        return this.color + ' ' + this.type + ' apple';
    };
}

var apple = new Apple('macintosh');


// A drawback of 1.1. is that the method getInfo() is recreated every 
// time you create a new object. Sometimes that may be what you want, 
// but it's rare. A more inexpensive way is to add getInfo() to the 
// prototype of the constructor function.

function Apple (type) {
    this.type = type;
    this.color = "red";
}
 
Apple.prototype.getInfo = function() {
    return this.color + ' ' + this.type + ' apple';
};

var apple = new Apple('macintosh');


// 2. Using object literals
// 
// Such an object is also sometimes called singleton. In "classical" 
// languages such as Java, singleton means that you can have only one 
// single instance of this class at any time, you cannot create more 
// objects of the same class. In JavaScript (no classes, remember?) 
// this concept makes no sense anymore since all objects are singletons 
// to begin with. 

var apple = {
    type: "macintosh",
    color: "red",
    getInfo: function () {
        return this.color + ' ' + this.type + ' apple';
    }
}


// 3. Singleton using a function
 

var apple = new function() {
    this.type = "macintosh";
    this.color = "red";
    this.getInfo = function () {
        return this.color + ' ' + this.type + ' apple';
    };
}

// 


apple.color = "reddish";
alert(apple.getInfo());

