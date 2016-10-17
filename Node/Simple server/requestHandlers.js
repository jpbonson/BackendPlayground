var querystring = require("querystring");
var fs = require("fs");
var exec = require("child_process").exec;
var formidable = require("formidable");

function start(response) {
    console.log("Request handler 'start' was called.");
    var body = '<html>'+
    '<head>'+
    '<meta http-equiv="Content-Type" content="text/html; '+
    'charset=UTF-8" />'+
    '</head>'+
    '<body>'+
    '<form action="/upload" method="post">'+
    '<textarea name="text" rows="20" cols="60"></textarea>'+
    '<input type="submit" value="Submit text" />'+
    '</form>'+
    '</body>'+
    '</html>';
    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(body);
    response.end();
}

function upload(response, request, postData) {
    console.log("Request handler 'upload' was called.");
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("You've sent: " + querystring.parse(postData).text);
    response.end();
}

function start_image(response) {
    console.log("Request handler 'start_image' was called.");
    var body = '<html>'+
    '<head>'+
    '<meta http-equiv="Content-Type" '+
    'content="text/html; charset=UTF-8" />'+
    '</head>'+
    '<body>'+
    '<form action="/upload_image" enctype="multipart/form-data" '+
    'method="post">'+
    '<input type="file" name="upload" multiple="multiple">'+
    '<input type="submit" value="Upload file" />'+
    '</form>'+
    '</body>'+
    '</html>';
    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(body);
    response.end();
}

function upload_image(response, request, postData) {
    console.log("Request handler 'upload_image' was called.");
    var form = new formidable.IncomingForm();
    console.log("about to parse");
    form.parse(request, function(error, fields, files) {
        console.log("parsing done");
        /* Possible error on Windows systems:
        tried to rename to an already existing file */
        fs.rename(files.upload.path, "./tmp/test.png", function(error) {
            if (error) {
                fs.unlink("./tmp/test.png");
                fs.rename(files.upload.path, "./tmp/test.png");
            }
        });
        response.writeHead(200, {"Content-Type": "text/html"});
        response.write("received image:<br/>");
        response.write("<img src='/show' />");
        response.end();
    });
}

function show(response) {
    console.log("Request handler 'show' was called.");

    response.writeHead(200, {"Content-Type": "image/jpeg"});
    fs.createReadStream("./tmp/images.jpeg").pipe(response);

    // alternatives: 
    
    // fs.readFile('./tmp/images.jpeg', function(err, data) {
    //     if (err) throw err; // Fail if the file can't be read.
    //     response.writeHead(200, {'Content-Type': 'image/jpeg'});
    //     response.end(data); // Send the file data to the browser.
    // });
     
    // fs.readFile('./tmp/images.jpeg', function(err, data) {
    //     if (err) throw err; // Fail if the file can't be read.
    //     response.writeHead(200, {'Content-Type': 'text/html'});
    //     response.write('<html><body><img src="data:image/jpeg;base64,')
    //     response.write(new Buffer(data).toString('base64'));
    //     response.end('"/></body></html>');
    // }); 
}

function list(response) {
    console.log("Request handler 'list' was called.");
    
    exec("ls -lah", function (error, stdout, stderr) {
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(stdout);
        response.end();
    });   
}

exports.start = start;
exports.upload = upload;
exports.start_image = start_image;
exports.upload_image = upload_image;
exports.show = show;
exports.list = list;