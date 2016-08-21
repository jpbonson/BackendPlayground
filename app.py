from flask import Flask, jsonify, abort, request
from tinydb import Query, where
import config

app = Flask(__name__)
config.configure_app(app)

def get_table(table_name):
    return app.config['DATABASE'].table(table_name)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(get_table('users').all())

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    query = Query()
    result = get_table('users').search(query.id == user_id)
    if len(result) == 0:
        abort(404)
    return jsonify(result[0])

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'id' in request.json:
        abort(400)
    query = Query()
    result = get_table('users').search(query.id == request.json['id'])
    if len(result) > 0:
        abort(409)
    user = {
        'id': request.json['id']
    }
    get_table('users').insert(user)
    return jsonify(user), 201

@app.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = get_table('users').remove(where('id') == user_id)
    if len(result) == 0:
        abort(404)
    return jsonify({'result': True})

@app.route('/stats/<string:url_id>', methods=['GET'])
def get_url(url_id):
    query = Query()
    result = get_table('urls').search(query.id == url_id)
    if len(result) == 0:
        abort(404)
    result[0].pop("userId")
    return jsonify(result[0])

@app.route('/users/<string:user_id>/urls', methods=['POST'])
def create_url(user_id):
    if not request.json or not 'url' in request.json:
        abort(400)
    query = Query()
    result = get_table('users').search(query.id == user_id)
    if len(result) == 0:
        abort(404)
    url = {
        "id": "23094", # TODO
        "hits": 0, #TODO
        "url": request.json['url'],
        "shortUrl": "http://"+request.host+"/"+"shorturl", #TODO
        "userId": user_id
    }
    get_table('urls').insert(url)
    url.pop("userId")
    return jsonify(url), 201

@app.route('/urls/<string:url_id>', methods=['DELETE'])
def delete_url(url_id):
    result = get_table('urls').remove(where('id') == url_id)
    if len(result) == 0:
        abort(404)
    return jsonify([])

if __name__ == "__main__":
    app.run()