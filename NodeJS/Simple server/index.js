var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;
handle["/start_image"] = requestHandlers.start_image;
handle["/upload_image"] = requestHandlers.upload_image;
handle["/show"] = requestHandlers.show;
handle["/list"] = requestHandlers.list;

server.start(router.route, handle);

// page 49 do pdf