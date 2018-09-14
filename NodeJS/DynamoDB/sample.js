'use strict';

var vogels = require('vogels'),
    util   = require('util'),
    _      = require('lodash'),
    async  = require('async'),
    Joi    = require('joi');
const Bluebird = require('bluebird');

Bluebird.promisifyAll(require('vogels/lib/table').prototype);
Bluebird.promisifyAll(require('vogels/lib/item').prototype);
Bluebird.promisifyAll(require('vogels/lib/query').prototype);
Bluebird.promisifyAll(require('vogels/lib/scan').prototype);
Bluebird.promisifyAll(require('vogels/lib/parallelScan').prototype);

const vogelsModel = vogels.model;
vogels.model = function promisifyModel(name, model) {
    if (model) {
        Bluebird.promisifyAll(model);
    }
    return vogelsModel.apply(vogels, arguments);
};

vogels.AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION,
    endpoint: 'http://localhost:4761'
});

var Movie = vogels.define('example-nested-attribute', {
  hashKey : 'title',
  timestamps : true,
  schema : {
    title       : Joi.string(),
    releaseYear : Joi.number(),
    tags        : vogels.types.stringSet(),
    director    : Joi.object().keys({
      firstName : Joi.string(),
      lastName  : Joi.string(),
      titles    : Joi.array()
    })
  }
});

var printResults = function (err, data) {
  console.log('----------------------------------------------------------------------');
  if(err) {
    console.log('Error - ', err);
  } else {
    console.log('Movie - ', util.inspect(data.get(), {depth : null}));
  }
  console.log('----------------------------------------------------------------------');
};

var printResults2 = function (err, data) {
  console.log('----------------------------------------------------------------------');
  if(err) {
    console.log('Error - ', err);
  } else {
    console.log('Movie - ', util.inspect(data.get()['attrs'], {depth : null}));
  }
  console.log('----------------------------------------------------------------------');
};

var loadSeedData = function (callback) {
  callback = callback || _.noop;

  async.times(10, function(n, next) {
    var director = { firstName : 'Steven', lastName : 'Spielberg the ' + n, titles : ['Producer', 'Writer', 'Director']};

    var tags = ['tag ' + n];

    if(n %3 === 0) {
      tags.push('Action');
    }

    if(n %5 === 0) {
      tags.push('Comedy');
    }

    Movie.create({title : 'Movie ' + n, releaseYear : 2001 + n, director : director, tags: tags}, next);
  }, callback);
};

function prettyPrint(obj) {
    console.log(JSON.stringify(obj, undefined, 2)+'\n');
}

var runExample = function () {

  // Movie.create({
  //   title : 'Star Wars: Episode IV - A New Hope',
  //   releaseYear : 1977,
  //   director : {
  //     firstName : 'George', lastName : 'Lucas', titles : ['Director']
  //   },
  //   tags : ['Action', 'Adventure']
  // }, printResults);

  // var params = {};
  // params.UpdateExpression = 'SET #year = #year + :inc, #dir.titles = list_append(#dir.titles, :title)';
  // params.ConditionExpression = '#year = :current';
  // params.ExpressionAttributeNames = {
  //   '#year' : 'releaseYear',
  //   '#dir' : 'director'
  // };
  // params.ExpressionAttributeValues = {
  //   ':inc' : 1,
  //   ':current' : 2001,
  //   ':title' : ['The Man']
  // };

  // Movie.get({title : 'Movie 0'}, printResults);
  // Movie.update({title : 'Movie 0'}, params, printResults);

  var params = {};
  params.UpdateExpression = 'SET #year = #year + :inc';
  // params.ConditionExpression = '#year = :current';
  params.ExpressionAttributeNames = {
    '#year' : 'releaseYear'
  };
  params.ExpressionAttributeValues = {
    ':inc' : 1
  };

  var dir = { firstName : 'Steven', lastName : 'Spielberg the Bullshit', titles : ['Producer', 'Writer', 'Director']}
  var tags = ['tag '];
  Movie.deleteTableAsync()
    .catch(() => null) // ignore errors
    .then(() => Movie.createTableAsync())
    .then(() => Movie.createAsync({title : 'Movie ', releaseYear : 2001, director: dir, tags: tags}))
    .then(() => Movie.getAsync({title : 'Movie '}))
    .tap(obj => prettyPrint(obj))
    .then(obj => obj.set({title: 'Bullshit: The Return'}))
    .then(obj => obj.updateAsync(params)) // {expected: {updatedAt: null}}
    .tap(obj => prettyPrint(obj))
    .then(() => {})
    .catch(err => {
        console.log('erro');
        console.log(err);
    });
};

// async.series([
//   async.apply(vogels.createTables.bind(vogels)),
//   loadSeedData
// ], function (err) {
//   if(err) {
//     console.log('error', err);
//     process.exit(1);
//   }

runExample();
// });
