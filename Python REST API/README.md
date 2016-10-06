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

### Users

Create new user
```
curl -i -H "Content-Type: application/json" -X POST -d '{"id":"maria"}' http://localhost:5000/users
```

List of users
```
curl -i -H "Content-Type: application/json" http://localhost:5000/users
```

Get user
```
curl -i -H "Content-Type: application/json" http://localhost:5000/users/maria
```

Delete user
```
curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/user/maria
```

### URLs

Create new URL
```
curl -i -H "Content-Type: application/json" -X POST -d '{"url":"https://google.com/"}' http://localhost:5000/users/maria/urls
```
Sample Result
```
{
  "hits": 0, 
  "id": "OA==", 
  "shortUrl": "http://localhost:5000/OA==", 
  "url": "https://google.com/"
}
```

Use short URL
```
curl -i http://localhost:5000/OA==
```

Delete URL
```
curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/urls/OA==
```

### Stats

About URL
```
curl -i -H "Content-Type: application/json" http://localhost:5000/stats/OA==
```

About user
```
curl -i -H "Content-Type: application/json" http://localhost:5000/users/maria/stats
```

About global usage
```
curl -i -H "Content-Type: application/json" http://localhost:5000/stats
```