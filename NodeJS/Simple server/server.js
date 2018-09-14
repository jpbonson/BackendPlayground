var formidable = require("formidable");
var http = require("http");
var url = require("url");
// var sys = require('sys');

function start(route, handle) {
    function onRequest(request, response) {
        var postData = "";
        var pathname = url.parse(request.url).pathname;
        console.log("Request for " + pathname + " received.");

        // request.setEncoding("utf8");
        // 
        // request.addListener("data", function(postDataChunk) {
        //     postData += postDataChunk;
        //     console.log("Received event: POST data chunk '"+postDataChunk+"'.");
        // });
        // 
        // request.addListener("end", function() {
        //     console.log("Received event: 'end'.");
        //     route(handle, pathname, response, request, postData);
        // });
        
        route(handle, pathname, response, request, postData);
    }

    http.createServer(onRequest).listen(8888);
    console.log("Server has started.");
}

exports.start = start;