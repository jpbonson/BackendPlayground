from flask import Flask, jsonify, abort, request, redirect
from tinydb import Query, where
import config

app = Flask(__name__)
config.configure_app(app)

def get_table(table_name):
    return app.config['DATABASE'].table(table_name)


# USER ROUTES

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(get_table('users').all())

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    result = get_table('users').search(Query().id == user_id)
    if len(result) == 0:
        abort(404)
    return jsonify(result[0])

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'id' in request.json:
        abort(400)
    result = get_table('users').search(Query().id == request.json['id'])
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
    return jsonify([])


# URL ROUTES

def redirect_url(url_id):
    result = get_table('urls').search(Query().id == url_id)
    if len(result) == 0:
        abort(404)
    url = result[0]["url"]
    hits = result[0]["hits"] + 1
    get_table('urls').update({'hits': hits}, Query().id == url_id)
    return url

@app.route('/urls/<string:url_id>')
def redirect_url_v1(url_id):
    url = redirect_url(url_id)
    return redirect(url, code=301)

@app.route('/<string:url_id>')
def redirect_url_v2(url_id):
    url = redirect_url(url_id)
    return redirect(url, code=301)

@app.route('/users/<string:user_id>/urls', methods=['POST'])
def create_url(user_id):
    if not request.json or not 'url' in request.json:
        abort(400)
    result = get_table('users').search(Query().id == user_id)
    if len(result) == 0:
        abort(404)
    url_id = "11111" # TODO
    url = {
        "id": url_id,
        "hits": 0,
        "url": request.json['url'],
        "shortUrl": "http://"+request.host+"/"+url_id,
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


# STATS ROUTES

def get_stats_for_urls(urls):
    total_hits = sum([x['hits'] for x in urls])
    sorted_urls = sorted(urls, key=lambda url: url['hits'], reverse=True)
    top10_urls = sorted_urls[0:10]
    [x.pop("userId") for x in top10_urls]
    result = {
        "hits": total_hits,
        "urlCount": len(urls),
        "topUrls": top10_urls,
    }
    return result

@app.route('/stats/<string:url_id>', methods=['GET'])
def get_url_stats(url_id):
    result = get_table('urls').search(Query().id == url_id)
    if len(result) == 0:
        abort(404)
    result[0].pop("userId")
    return jsonify(result[0])

@app.route('/users/<string:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    query = Query()
    result = get_table('users').search(query.id == user_id)
    if len(result) == 0:
        abort(404)
    urls = get_table('urls').search(query.userId == user_id)
    result = get_stats_for_urls(urls)
    return jsonify(result)

@app.route('/stats', methods=['GET'])
def get_global_stats():
    all_urls = get_table('urls').all()
    result = get_stats_for_urls(all_urls)
    return jsonify(result)

if __name__ == "__main__":
    app.run()