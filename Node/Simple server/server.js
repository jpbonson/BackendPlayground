var formidable = require("formidable");
var http = require("http");
var url = require("url");
// var sys = require('sys');

function start(route, handle) {
    function onRequest(request, response) {
        var postData = "";
        var pathname = url.parse(request.url).pathname;
        console.log("Request for " + pathname + " received.");

        request.setEncoding("utf8");

        request.addListener("data", function(postDataChunk) {
            postData += postDataChunk;
            console.log("Received event: POST data chunk '"+postDataChunk+"'.");
        });

        request.addListener("end", function() {
            console.log("Received event: 'end'.");
            route(handle, pathname, response, postData);
        });
    }

    http.createServer(onRequest).listen(8888);
    console.log("Server has started.");
}

exports.start = start;


// http.createServer(function(req, res) {
// if (req.url == '/upload' && req.method.toLowerCase() == 'post') {
// // parse a file upload
// var form = new formidable.IncomingForm();
// form.parse(req, function(error, fields, files) {Building the application stack
// res.writeHead(200, {'content-type': 'text/plain'});
// res.write('received upload:\n\n');
// res.end(sys.inspect({fields: fields, files: files}));
// });
// return;
// 10
// 11
// 12
// 13
// 14
// 15
// 41
// }
// 16
// 17
// 18
// 19
// 20
// 21
// 22
// 23
// 24
// 25
// 26
// 27
// // show a file upload form
// res.writeHead(200, {'content-type': 'text/html'});
// res.end(
// '<form action="/upload" enctype="multipart/form-data" '+
// 'method="post">'+
// '<input type="text" name="title"><br>'+
// '<input type="file" name="upload" multiple="multiple"><br>'+
// '<input type="submit" value="Upload">'+
// '</form>'
// );
// }).listen(8888);