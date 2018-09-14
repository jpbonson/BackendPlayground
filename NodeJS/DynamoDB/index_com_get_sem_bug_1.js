'use strict';

const Bluebird = require('bluebird');
const Joi = require('joi');
const vogels = require('vogels');

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

const Account = vogels.define('Account', {
    hashKey: 'email',
    timestamps: true,
    schema: {
        email: Joi.string().email(),
        name: Joi.string(),
        settings: {
            nickname: Joi.string(),
            lastname: Joi.string(),
            terms: {
                version: Joi.string(),
                accepted: Joi.boolean().default(false)
            }
        }
    }
});

const account = {
    email: 'xpto@gmail.com',
    name: 'xpto',
    settings: {
        nickname: 'snoopy',
        lastname: 'dog',
        terms: {
            version: '1',
            accepted: true
        }
    },
    updatedAt: new Date(1900).toISOString() // "2010-10-27T17:54:03.555Z"
};

function prettyPrint(label, obj) {
    console.log(label+': '+JSON.stringify(obj, undefined, 2)+'\n');
}

Account.deleteTableAsync()
    .catch(() => null) // ignore errors
    .then(() => Account.createTableAsync())
    .then(() => Account.createAsync(account))
    .tap(obj => prettyPrint('original', obj))
    // .then(obj => obj.set({name: 'name'}))
    // .then(obj => obj.updateAsync())
    // .tap(obj => prettyPrint('after update 1', obj))



    // .then(obj => obj.set({name: 'name2'}))
    // .then(obj => obj.updateAsync())
    // .tap(obj => prettyPrint('after update 2', obj))
    // .then(obj => obj.set({name: 'name3'}))
    // .then(obj => {
    //     delete obj.attrs.updatedAt;
    //     return Account.updateAsync(obj.attrs);
    // })
    // .tap(obj => prettyPrint('after update 3', obj))
    // .then(obj => Account.updateAsync({email: 'xpto@gmail.com'}))
    // .tap(obj => prettyPrint('after update 4', obj))
    // .then(() => Account.getAsync('xpto@gmail.com'))
    // .tap(obj => prettyPrint('final', obj))
    .then(() => {
    })
    .catch(err => {
        console.log('erro');
        console.log(err);
    });