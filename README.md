# ShortURLsAPI

API that shortens URLs. The URLs are stored per user, along with usage statistics.

Implemented in Python, with the Flask web framework.


## Index
1. How to Install
2. How to Run
3. How to Test
4. Architecture
5. How to Use

## 1. How to Install

```
sh install.sh
```

## 2. How to Run

To execute for production:
```
sh start.sh
```

To execute for development:
```
python app.py
```

## 3. How to Test

```
nosetests
```

## 4. Architecture

* The main file is 'app.py', it contains all the routes served by the API.
* All the configurations are available in 'config.py', for development, testing, and production.
* The data is stored on TinyDB, a simple JSON database.
* The main route (GET /urls/:id) is cached to improve performance.
* The web server uses Flask, a lightweight Python web framework based on Werkzeug and Jinja 2.
* All the tests are on /tests, separated per type of route that is being tested.

## 5. How to Use

[TODO]