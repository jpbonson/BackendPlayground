'use strict';

const Bluebird = require('bluebird');
const Joi = require('joi');
const vogels = require('vogels');
const _ = require('lodash');
var retry = require('bluebird-retry');

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
        // was_updated: Joi.boolean().default(false),
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

function prettyPrint(label, obj) {
    console.log(label+': '+JSON.stringify(obj, undefined, 2)+'\n');
}

let changes1 = {settings: {nickname: 'blah6'}, was_updated: true}
let changes2 = {name: 'blah', was_updated: true}

function something1() {
    let createdAt1;
    let updatedAt1;
    let controlKey1;
    return Account.getAsync('xpto@gmail.com')
        .tap(obj => prettyPrint('2 obj in bd', obj))
        .then(obj => {
            createdAt1 = obj['attrs']['createdAt'];
            updatedAt1 = obj['attrs']['updatedAt'];
            controlKey1 = {}
            if ('updatedAt' in obj['attrs']) {
                console.log('updatedAt1: '+updatedAt1);
                controlKey1 = {updatedAt: updatedAt1}
            }
            obj.set(changes1);
            return obj;
        })
        .then(obj => {
            delete obj.attrs.updatedAt;
            return obj.updateAsync({expected: controlKey1})
            // return Account.updateAsync(obj.attrs, {expected: controlKey1})
        })
        .tap(obj => prettyPrint('2 obj after update', obj))
}

function something2() {
    let createdAt2;
    let updatedAt2;
    let controlKey2;
    return Account.getAsync('xpto@gmail.com')
        .tap(obj => prettyPrint('3 obj in bd', obj))
        .then(obj => {
            createdAt2 = obj['attrs']['createdAt'];
            updatedAt2 = obj['attrs']['updatedAt'];
            controlKey2 = {}
            if ('updatedAt' in obj['attrs']) {
                console.log('updatedAt2: '+updatedAt2);
                controlKey2 = {updatedAt: updatedAt2}
            }
            obj.set(changes2);
            return obj;
        })
        .then(obj => {
            delete obj.attrs.updatedAt;
            return obj.updateAsync({expected: controlKey2})
            // return Account.updateAsync(obj.attrs, {expected: controlKey2})
        })
        .tap(obj => prettyPrint('3 obj after update', obj))
}

let cont = 0
while (cont < 2) {
    retry(something1, { max_tries: 4, interval: 500 });
    retry(something2, { max_tries: 4, interval: 500 });
    // something1()
    // something2()
    cont++;
}