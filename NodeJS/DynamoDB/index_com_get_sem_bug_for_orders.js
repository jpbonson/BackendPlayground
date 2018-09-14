'use strict';

const Bluebird = require('bluebird');
const Joi = require('joi');
const vogels = require('vogels');
const _ = require('lodash');

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

const telephone = {
    description: Joi.string().empty(''),
    countryCode: Joi.string().empty(''),
    number: Joi.string().required(),
    type: Joi.string().required()
};

const doc = {
    type: Joi.string().required(),
    number: Joi.string().required()
};

const address = {
    address1: Joi.string(),
    address2: Joi.string().empty(''),
    city: Joi.string(),
    country: Joi.string(),
    description: Joi.string().empty(''),
    district: Joi.string(),
    firstName: Joi.string(),
    lastName: Joi.string(),
    neighbourhood: Joi.string(),
    number: Joi.string(),
    telephone,
    state: Joi.string(),
    zip: Joi.string(),
    defaultBilling: Joi.boolean().default(false),
    defaultShipping: Joi.boolean().default(false),
    status: Joi.string().valid('ACTIVE', 'INACTIVE')
};

const Order = vogels.define('Order', {
    hashKey: 'hubId',
    timestamps: true,
    tableName: 'testing-chubaca-orders',
    schema: {
        id: Joi.string().required(),
        channelId: Joi.string().required(),
        clientId: Joi.string().required(),
        hubId: Joi.string().required(),
        backOfficeId: Joi.string().empty(''),
        // FIXME CHUB-320
        status: Joi.string().required(),
        placedAt: Joi.string().required(),
        total: Joi.number().required(),
        discount: Joi.number().default(0).min(0),
        customer: {
            id: Joi.string().required(),
            firstName: Joi.string().required(),
            lastName: Joi.string().empty(''),
            email: Joi.string().email().required(),
            birthdate: Joi.string().isoDate().empty(''),
            addresses: Joi.object().pattern(/.*/, address),
            gender: Joi.string().valid('F', 'M').empty(''),
            telephones: Joi.array().items(telephone), // FIXME CHUB-222
            documents: Joi.array().items(doc), // FIXME CHUB-222
            type: Joi.string().valid('INDIVIDUAL', 'LEGAL').default('INDIVIDUAL'),
            registeredAt: Joi.string().isoDate()
        },
        shipments: Joi.array().items(Joi.object().keys({
            address,
            method: Joi.string().required(),
            basePrice: Joi.number().required(),
            discount: Joi.number().default(0),
            tracking: Joi.string(),
            total: Joi.number().required()
        })),
        invoices: Joi.array().items(Joi.object().keys({
            id: Joi.string(),
            issuedAt: Joi.string()
        })),
        payments: Joi.array().items(Joi.object().keys({
            paymentNumber: Joi.number().required(),
            type: Joi.string().valid('BOLETO', 'CREDIT_CARD', 'CUSTOMER_CREDIT').required(),
            amount: Joi.number().required(),
            currency: Joi.string().required().default('BRL')
        }).unknown()), // FIXME CHUB-237
        billingAddress: address,
        items: Joi.array().items(Joi.object().keys({
            sku: Joi.string().required(),
            quantity: Joi.number(),
            discount: Joi.number().default(0),
            basePrice: Joi.number(),
            price: Joi.number()
        })),
        fulfillment: {
            reconciledAt: Joi.string().isoDate().empty(''),
            location: Joi.string().empty('')
        },
        connectorStatus: {}
    },
    indexes: [
        {
            name: 'BackOfficeIndex',
            hashKey: 'backOfficeId',
            rangeKey: 'clientId',
            type: 'global'
        }
    ]
});

const order = {
  "backOfficeId": "-50508",
  "billingAddress": {
    "address1": "Rua Mateus Grou",
    "address2": "lado par",
    "city": "São Paulo",
    "country": "BR",
    "defaultBilling": false,
    "defaultShipping": false,
    "description": "Casa",
    "firstName": "Fabio",
    "lastName": "Coutinho",
    "neighbourhood": "Pinheiros",
    "number": "57",
    "state": "São Paulo",
    "telephone": {
      "number": "11949807747",
      "type": "billing"
    },
    "zip": "05415-040"
  },
  "channelId": "site",
  "clientId": "procorrer",
  // "connectorStatus": {
  //   "b2cmanager": "OK"
  // },
  "createdAt": "2016-09-12T13:26:14.296Z",
  "customer": {
    "documents": [
      {
        "number": "Mg13151158",
        "type": "rg"
      },
      {
        "number": "16802774801",
        "type": "cpf"
      }
    ],
    "email": "fabio.coutinho@neemu.com.br",
    "firstName": "Fabio",
    "gender": "M",
    "id": "16802774801",
    "lastName": "Coutinho",
    "type": "INDIVIDUAL"
  },
  "discount": 74.96,
  "fulfillment": {
    "location": "000004",
    "reconciledAt": "1900-01-01T00:00:00Z"
  },
  "hubId": "procorrer-site-000040126",
  "id": "000040126",
  "items": [
    {
      "basePrice": 499.9,
      "discount": 74.96,
      "price": 149.92,
      "quantity": 1,
      "sku": "01011414_0793_21"
    }
  ],
  "payments": [
    {
      "amount": 80.96,
      "boletoBank": "341",
      "boletoCode": "000040126",
      "boletoExpiresAt": "2016-09-18T02:59:59Z",
      "currency": "BRL",
      "isCaptured": false,
      "paymentNumber": 1,
      "type": "BOLETO"
    }
  ],
  "placedAt": "2016-09-12T16:25:51Z",
  "shipments": [
    {
      "address": {
        "address1": "Rua Mateus Grou",
        "address2": "lado par",
        "city": "São Paulo",
        "country": "BR",
        "defaultBilling": false,
        "defaultShipping": false,
        "description": "Casa",
        "firstName": "Fabio",
        "lastName": "Coutinho",
        "neighbourhood": "Pinheiros",
        "number": "57",
        "state": "São Paulo",
        "telephone": {
          "number": "11949807747",
          "type": "shipment"
        },
        "zip": "05415-040"
      },
      "basePrice": 6,
      "discount": 0,
      "method": "omsshipping_CORREIOS|E-SEDEX",
      "total": 6
    }
  ],
  "status": "CANCELED",
  "total": 149.92,
  "updatedAt": "2016-09-12T13:26:15.423Z"
};

const order2 = {
  "backOfficeId": "-50508",
  "billingAddress": {
    "address1": "Rua Mateus Grou",
    "address2": "lado par",
    "city": "São Paulo",
    "country": "BR",
    "defaultBilling": false,
    "defaultShipping": false,
    "description": "Casa",
    "firstName": "Fabio",
    "lastName": "Coutinho",
    "neighbourhood": "Pinheiros",
    "number": "57",
    "state": "São Paulo",
    "telephone": {
      "number": "11949807747",
      "type": "billing"
    },
    "zip": "05415-040"
  },
  "channelId": "site",
  "clientId": "procorrer",
  // "connectorStatus": {
  //   "b2cmanager": "OK"
  // },
  "createdAt": "2016-09-12T13:26:14.296Z",
  "customer": {
    "documents": [
      {
        "number": "Mg13151158",
        "type": "rg"
      },
      {
        "number": "16802774801",
        "type": "cpf"
      }
    ],
    "email": "fabio.coutinho@neemu.com.br",
    "firstName": "Fabio",
    "gender": "M",
    "id": "16802774801",
    "lastName": "Coutinho",
    "type": "INDIVIDUAL"
  },
  "discount": 74.96,
  "fulfillment": {
    "location": "far_away",
    "reconciledAt": "1900-01-01T00:00:00Z"
  },
  "hubId": "procorrer-site-000040126",
  "id": "000040126",
  "items": [
    {
      "basePrice": 499.9,
      "discount": 74.96,
      "price": 149.92,
      "quantity": 1,
      "sku": "01011414_0793_21"
    }
  ],
  "payments": [
    {
      "amount": 80.96,
      "boletoBank": "341",
      "boletoCode": "000040126",
      "boletoExpiresAt": "2016-09-18T02:59:59Z",
      "currency": "BRL",
      "isCaptured": false,
      "paymentNumber": 1,
      "type": "BOLETO"
    }
  ],
  "placedAt": "2016-09-12T16:25:51Z",
  "shipments": [
    {
      "address": {
        "address1": "Rua Mateus Grou",
        "address2": "lado par",
        "city": "São Paulo",
        "country": "BR",
        "defaultBilling": false,
        "defaultShipping": false,
        "description": "Casa",
        "firstName": "Fabio",
        "lastName": "Coutinho",
        "neighbourhood": "Pinheiros",
        "number": "57",
        "state": "São Paulo",
        "telephone": {
          "number": "11949807747",
          "type": "shipment"
        },
        "zip": "05415-040"
      },
      "basePrice": 6,
      "discount": 0,
      "method": "omsshipping_CORREIOS|E-SEDEX",
      "total": 6
    }
  ],
  "status": "CANCELED",
  "total": 149.92,
  "updatedAt": "2016-09-12T13:26:15.423Z"
};

function prettyPrint(label, obj) {
    console.log(label+': '+JSON.stringify(obj, undefined, 2)+'\n');
}

function getDifference(a, b) {
        return _.reduce(a, (result, value, key) => {
            if (_.isEqual(value, b[key])) {
                return result;
            }

            return result.concat(key);
        }, []);
    }

Order.deleteTableAsync()
    .catch(() => null) // ignore errors
    .then(() => Order.createTableAsync())
    .then(() => Order.createAsync(order))
    .tap(obj => prettyPrint('original', obj))
    .then(() => Order.getAsync('procorrer-site-000040126'))
    .tap(obj => prettyPrint('obj in bd 1', obj))
    .then(obj => obj.set({fulfillment: {location: 'pqp'}}))
    .then(obj => obj.updateAsync())
    // .then(dynamoResponse => {
    //     // orderNotificationService.notify(dynamoResponse.attrs, oldOrder);
    //     console.log('whatever: '+JSON.stringify(dynamoResponse.attrs));
    //     return dynamoResponse.attrs;
    // })
    .tap(obj => prettyPrint('obj after update', obj))
    .then(() => Order.getAsync('procorrer-site-000040126'))
    .tap(obj => prettyPrint('obj in bd 2', obj))
    .then(obj => {
        // console.log(getDifference(order, order2));
        // console.log(JSON.stringify(Object.prototype.toString.call(order)));
        // console.log(JSON.stringify(Object.prototype.toString.call(obj)));
        // console.log('A');
        // obj.set({fulfillment: {location: 'pqp1'}});
        // console.log('B');
        // JSON.stringify(order).set({fulfillment: {location: 'pqp2'}});
        // console.log('C');
        // order.set({fulfillment: {location: 'pqp2'}});
        // console.log('D');
    })
    .catch(err => {
        console.log('erro');
        console.log(err);
    });



