[![Build Status](https://circleci.com/gh/jpbonson/work-at-olist.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/jpbonson/)

# Call Records API #

A Python REST API that receives call detail records and calculates monthly bills for a given telephone number.

Python3. Django. REST API. PostgreSQL. Heroku.

Work Environment: Notebook HP, Ubuntu 16.04 LTS, Sublime 3

Data Model study: https://drive.google.com/file/d/1lmXnpRfOzIfzDM44R_PCjvJe5Q4K8hMU/view?usp=sharing

Obs.: To avoid taking too much time to finish the project, the API documentation is simpler and listed in this README. Ideally, I would produce a more complete API doc (generated using Swagger, for example).

### How to install? ###

```
pipenv install
python manage.py makemigrations
python manage.py migrate
export DJANGO_SETTINGS_MODULE=call_records_api.settings
```

### How to run? ###

```
gunicorn call_records_api.wsgi
```

### How to test? ###

```
python manage.py test
```

### API Routes ###

Application: https://rocky-waters-86988.herokuapp.com/

## Subscribers

- GET (list)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/subscribers/
```

- POST (create)
```
curl -u admin:dev123456 -d '{"name":"Ana", "phone":48988526423}' -H "Content-Type: application/json" -X POST https://rocky-waters-86988.herokuapp.com/v1/subscribers/
```

- GET (individual)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/subscribers/1/
```

- PUT/PATCH (update)
```
curl -u admin:dev123456 -d '{"name":"Ana", "phone":12341234}' -H "Content-Type: application/json" -X PUT https://rocky-waters-86988.herokuapp.com/v1/subscribers/1/
```

- DELETE (remove)
```
curl -u admin:dev123456 -X "DELETE" https://rocky-waters-86988.herokuapp.com/v1/subscribers/1/
```

## CallRecords

- GET (list)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/callRecords/
```

- POST (create)
Call Start Record
```
curl -u admin:dev123456 -d '{"type": "start","timestamp": "2017-12-12T18:35:59Z","call_id": 77,"source": 48988526423,"destination": 4893468278}' -H "Content-Type: application/json" -X POST https://rocky-waters-86988.herokuapp.com/v1/callRecords/
```

Call End Record
```
curl -u admin:dev123456 -d '{"type": "end","timestamp": "2017-12-12T18:35:59Z","call_id": 77}' -H "Content-Type: application/json" -X POST https://rocky-waters-86988.herokuapp.com/v1/callRecords/
```

Obs.: Each pair of call start/end creates a BillRecord on DB for that call.

## Price Rates

- GET (list)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/priceRates/
```

- POST (create)
```
curl -u admin:dev123456 -d '{"rate_type": "std", "start_time": "06:00:00", "end_time": "22:00:00", "standing_charge": 0.36, "charge_per_min": 0.09}' -H "Content-Type: application/json" -X POST https://rocky-waters-86988.herokuapp.com/v1/priceRates/
```
```
curl -u admin:dev123456 -d '{"rate_type": "rdc", "start_time": "22:00:00", "end_time": "06:00:00", "standing_charge": 0.36, "charge_per_min": 0.00}' -H "Content-Type: application/json" -X POST https://rocky-waters-86988.herokuapp.com/v1/priceRates/
```

- GET (individual)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/priceRates/1/
```

- PUT/PATCH (update)
```
curl -u admin:dev123456 -d '{"rate_type": "std", "start_time": "12:00:00", "end_time": "02:00:00", "standing_charge": 0.04, "charge_per_min": 0.55}' -H "Content-Type: application/json" -X PUT https://rocky-waters-86988.herokuapp.com/v1/priceRates/1/
```

- DELETE (remove)
```
curl -u admin:dev123456 -X "DELETE" https://rocky-waters-86988.herokuapp.com/v1/priceRates/1/
```

## Bills Records

- GET (with reference_period assumed to be the last month)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/billRecords/48988526423/
```

- GET (with reference_period informed in the query)
```
curl -u admin:dev123456 https://rocky-waters-86988.herokuapp.com/v1/billRecords/48988526423/?reference=01-2014
```
