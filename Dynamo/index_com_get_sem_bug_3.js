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
    }
};

function prettyPrint(label, obj) {
    console.log(label+': '+JSON.stringify(obj, undefined, 2)+'\n');
}

let cont = 0
while (cont < 1000) {
    Account.getAsync('xpto@gmail.com')
        .tap(obj => prettyPrint('3 obj in bd', obj))
        .then(obj => obj.set({settings: {lastname: 'blah'}}))
        .then(obj => obj.updateAsync())
        .tap(obj => prettyPrint('3 obj after update', obj))
        .then(() => {
        })
        .catch(err => {
            console.log('erro');
            console.log(err);
        });
    cont++;
}