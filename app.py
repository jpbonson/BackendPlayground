from flask import Flask
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('db.json')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()