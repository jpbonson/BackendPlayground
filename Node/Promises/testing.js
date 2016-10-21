// http://stackoverflow.com/questions/14220321/how-do-i-return-the-response-from-an-asynchronous-call/16825593#16825593
// http://bluebirdjs.com/docs/working-with-callbacks.html
// https://developers.google.com/web/fundamentals/getting-started/primers/promises
// http://bluebirdjs.com/docs/api-reference.html
// http://stackoverflow.com/questions/29268569/what-is-the-correct-terminology-for-javascript-promises


// The Promise object is used for asynchronous computations. A Promise 
// represents a value which may be available now, or in the future, or never.



// ############### Promises with Bluebird

var Bluebird = require('bluebird');
var fs = Bluebird.promisifyAll(require('fs'));

// original
fs.readFile("file.json", function (err, val) {
    if (err) {
        console.error("unable to read file");
    }
    else {
        try {
            val = JSON.parse(val);
            console.log(val);
        }
        catch (e) {
            console.error("invalid json in file");
        }
    }
});

// with promises
fs.readFileAsync("file.json").then(JSON.parse).then(function (val) {
    console.log(val);
})
.catch(SyntaxError, function (e) {
    console.error("invalid json in file");
})
.catch(function (e) {
    console.error("unable to read file");
});









// ############### Native Promises in JS

// // original
// function((err, data) => { if (err) {} });

// // with promises
// function().then(data => {}).catch();




function delay() {
  // `delay` returns a promise
  return new Promise(function(resolve, reject) {
    // Only `delay` is able to resolve or reject the promise
    setTimeout(function() {
      resolve(42); // After 0.5 seconds, resolve the promise with value 42
    }, 500);
  });
}

delay().then(function(v) { // `delay` returns a promise
  console.log(v); // Log the value once it is resolved
}).catch(function(v) {
  // Or do something else if it is rejected 
  // (it would not happen in this example, since `reject` is not called).
});




var promise = new Promise(function(resolve, reject) {
  // do a thing, possibly async, then…
  var ok = true;
  if (ok) {
    resolve("Stuff worked!");
  }
  else {
    reject(Error("It broke"));
  }
});

promise.then(function(result) {
  console.log(result); // "Stuff worked!"
}, function(err) {
  console.log(err); // Error: "It broke"
});




var promise = new Promise(function(resolve, reject) {
  resolve(1);
});

promise.then(function(val) {
  console.log(val); // 1
  return val + 2;
}).then(function(val) {
  console.log(val); // 3
})




function get(url) {
  // Return a new promise.
  return new Promise(function(resolve, reject) {
    // Do the usual XHR stuff
    var req = new XMLHttpRequest();
    req.open('GET', url);

    req.onload = function() {
      // This is called even on 404 etc
      // so check the status
      if (req.status == 200) {
        // Resolve the promise with the response text
        resolve(req.response);
      }
      else {
        // Otherwise reject with the status text
        // which will hopefully be a meaningful error
        reject(Error(req.statusText));
      }
    };

    // Handle network errors
    req.onerror = function() {
      reject(Error("Network Error"));
    };

    // Make the request
    req.send();
  });
}




get('story.json').then(function(response) {
  return JSON.parse(response);
}).then(function(response) {
  console.log("Yey JSON!", response);
})
// equivalent:
get('story.json').then(JSON.parse).then(function(response) {
  console.log("Yey JSON!", response);
})
// 
// 
// When you return something from a then() callback, it's a bit magic. 
// If you return a value, the next then() is called with that value. 
// However, if you return something promise-like, the next then() waits 
// on it, and is only called when that promise settles (succeeds/fails). 
// For example:
function getJSON(url) { // getJSON() still returns a promise, one that fetches a url then parses the response as JSON.
  return get(url).then(JSON.parse);
}

getJSON('story.json').then(function(story) {
  return getJSON(story.chapterUrls[0]);
}).then(function(chapter1) {
  console.log("Got chapter 1!", chapter1);
})




// You could even make a shortcut method to get chapters:

var storyPromise;

function getChapter(i) {
  storyPromise = storyPromise || getJSON('story.json');

  return storyPromise.then(function(story) {
    return getJSON(story.chapterUrls[i]);
  })
}

// and using it is simple:
getChapter(0).then(function(chapter) {
  console.log(chapter);
  return getChapter(1);
}).then(function(chapter) {
  console.log(chapter);
})

// We don't download story.json until getChapter is called, but the 
// next time(s) getChapter is called we reuse the story promise, so 
// story.json is only fetched once. Yay Promises!






get('story.json').then(function(response) {
  console.log("Success!", response);
}, function(error) {
  console.log("Failed!", error);
})

// You can also use catch():

get('story.json').then(function(response) {
  console.log("Success!", response);
}).catch(function(error) {
  console.log("Failed!", error);
})

// There's nothing special about catch(), it's just sugar for 
// then(undefined, func), but it's more readable. Note that the two 
// code examples above do not behave the same, the latter is equivalent to:

get('story.json').then(function(response) {
  console.log("Success!", response);
}).then(undefined, function(error) {
  console.log("Failed!", error);
})

// The difference is subtle, but extremely useful. Promise rejections 
// skip forward to the next then() with a rejection callback (or catch(), 
// since it's equivalent). With then(func1, func2), func1 or func2 
// will be called, never both. But with then(func1).catch(func2), 
// both will be called if func1 rejects, as they're separate steps in 
// the chain.



// Rejections happen when a promise is explicitly rejected, but also 
// implicitly if an error is thrown in the constructor callback.

// This means it's useful to do all your promise-related work inside 
// the promise constructor callback, so errors are automatically caught 
// and become rejections.

// Like JavaScript's try/catch, the error is caught and subsequent code 
// continues.

function count(value) {
  return new Promise(function(resolve, reject) {
    value = value + 1;
    if (value < 15) {
        resolve(value);
    }
    else {
        reject(Error("It broke, bad value! Value: "+value));
    }
  });
}

var value = 0;
// var value = 10;
count(value).then(count).then(value => {
    console.log(value);
    return count(value);
}).then(count).then(count).then(count).catch(function(err) {
    console.log("Erro: "+err);
    return 1000;
}).then(value => {
    console.log(value);
    return count(value);
})







// ############### AJAX e QUERY


// function ajax(url) {
//   return new Promise(function(resolve, reject) {
//     var xhr = new XMLHttpRequest();
//     xhr.onload = function() {
//       resolve(this.responseText);
//     };
//     xhr.onerror = reject;
//     xhr.open('GET', url);
//     xhr.send();
//   });
// }

// ajax("/echo/json").then(function(result) {
//   // Code depending on result
//   console.log('A');
// }).catch(function() {
//   // An error occurred
//   console.log('B');
// });

// function foo() {
//     // RETURN the promise
//     return fetch("/echo/json").then(function(response){
//         return response.json(); // process it inside the `then`
//     });
// }
// foo().then(function(response){
//     // access the value inside the `then`
// })



// Keep in mind that promises and deferred objects are just containers 
// for a future value, they are not the value itself.



// // code that don't work as expected
// function checkPassword() {
//     return $.ajax({
//         url: '/password',
//         data: {
//             username: $('#username').val(),
//             password: $('#password').val()
//         },
//         type: 'POST',
//         dataType: 'json'
//     });
// }

// if (checkPassword()) {
//     // Tell the user they're logged in
// }

// // code that works
// checkPassword()
// .done(function(r) {
//     if (r) {
//         // Tell the user they're logged in
//     } else {
//         // Tell the user their password was bad
//     }
// })
// .fail(function(x) {
//     // Tell the user something bad happened
// });