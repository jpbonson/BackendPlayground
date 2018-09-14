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
        terms: {
            version: '1',
            accepted: true
        }
    }
};

const account2 = {
    email: 'xpto@gmail.com',
    name: 'xpto',
    settings: {
        nickname: 'snoopy',
        terms: {
            version: '2',
            accepted: true
        }
    }
};

function prettyPrint(label, obj) {
    console.log(label+': '+JSON.stringify(obj, undefined, 2)+'\n');
}

Account.deleteTableAsync()
    .catch(() => null) // ignore errors
    .then(() => Account.createTableAsync())
    .then(() => Account.createAsync(account))
    .tap(obj => prettyPrint('original', obj))
    .then(() => Account.updateAsync({email: 'xpto@gmail.com', name: 'Bar Tester'}))
    .tap(obj => prettyPrint('changed name', obj))
    .then(() => Account.updateAsync({email: 'xpto@gmail.com', settings: {terms: {version: 3}}}))
    .tap(obj => prettyPrint('changed version (bug)', obj))
    .then(() => Account.updateAsync(account))
    .tap(obj => prettyPrint('original', obj))
    .then(() => Account.updateAsync({email: 'xpto@gmail.com', settings: {nickname: 'bug'}}))
    .tap(obj => prettyPrint('changed nickname (bug)', obj))
    .then(() => Account.updateAsync(account))
    .tap(obj => prettyPrint('original', obj))
    .then(() => Account.updateAsync({email: 'xpto@gmail.com', settings: {nickname: 'bug'}}, {ReturnValues: 'ALL_OLD'}))
    .tap(obj => prettyPrint('changed nickname (bug?)', obj))
    .then(() => Account.getAsync('xpto@gmail.com'))
    .tap(obj => prettyPrint('obj in bd', obj))
    .then(() => {
    })
    .catch(err => {
        console.log('erro');
        console.log(err);
    });