var mongojs = require('mongojs');

var env = require('./env');

var db = mongojs(process.env.ip_addr+':27017/'+process.env.app_name, 
    [process.env.app_name]);
var jobs = db.collection('jobs');


function findAllJobs(req, res, next){
    res.setHeader('Access-Control-Allow-Origin','*');
    jobs.find().limit(20).sort({postedOn : -1} , function(err, success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            return next();
        }else{
            return next(err);
        }
 
    });
 
}
 
function findJob(req, res, next){
    res.setHeader('Access-Control-Allow-Origin','*');
    jobs.findOne({_id:mongojs.ObjectId(req.params.jobId)} , function(err, success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            return next();
        }
        return next(err);
    })
}
 
function postNewJob(req, res, next){
    var job = {};
    job.title = req.body.title;
    job.description = req.body.description;
    job.location = req.body.location;
    job.postedOn = new Date();
 
    res.setHeader('Access-Control-Allow-Origin','*');
 
    jobs.save(job , function(err, success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(201 , job);
            return next();
        }else{
            return next(err);
        }
    });
}
 
function deleteJob(req, res, next){
    res.setHeader('Access-Control-Allow-Origin','*');
    jobs.remove({_id:mongojs.ObjectId(req.params.jobId)}, function(err, success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(204);
            return next();      
        } else{
            return next(err);
        }
    })
 
}

exports.findAllJobs = findAllJobs
exports.findJob = findJob
exports.postNewJob = postNewJob
exports.postNewJob_express = postNewJob_express
exports.deleteJob = deleteJob