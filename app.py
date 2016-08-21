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

if __name__ == "__main__":
    app.run()