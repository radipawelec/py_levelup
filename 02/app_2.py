from flask import Flask, request, render_template, make_response, redirect, jsonify
from flask_basicauth import BasicAuth
 
app = Flask(__name__)
 
app.config['BASIC_AUTH_USERNAME'] = 'Akwarysta69'
app.config['BASIC_AUTH_PASSWORD'] = 'J3si07r'
 
basic_auth = BasicAuth(app)
 
fishes = {
    "id_1": {
        "who": "Znajomy",
        "where": {
            "lat": 0.001,
            "long": 0.002
        },
        "mass": 34.56,
        "length": 23.67,
        "kind": "szczupak"
    },
    "id_2": {
        "who": "Kolega kolegi",
        "where": {
            "lat": 34.001,
            "long": 52.002
        },
        "mass": 300.12,
        "length": 234.56,
        "kind": "sum olimpijczyk"
    }
}
 
 
@app.route('/')
def index():
    return 'Welcome!'
 
 
@app.route('/hello')
@basic_auth.required
def hello():
    cookie_secret = request.cookies.get('cookie_secret')
    auth = request.authorization
    if str(cookie_secret).__len__() > 1 and auth and auth.username == 'Akwarysta69' and auth.password == 'J3si07r':
        return make_response(render_template(
            'hello.html', cookie_secret=cookie_secret, user=auth.username
        ))
 
    return make_response('Could not verify your login', 401,
                                          {'WWW-Authenticate': 'Basic realm="Login Required"'})
 
 
@app.route('/login', methods=['POST'])
def log_in():
    auth = request.authorization
    if request.method == 'POST' and auth.username == 'Akwarysta69' and auth.password == 'J3si07r':
        resp = make_response(redirect('/hello'))
        resp.set_cookie('cookie_secret', 'I am new cookie')
        return resp
    return make_response('Could not verify your login', 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})
 
 
@app.route('/logout', methods=['POST'])
@basic_auth.required
def log_out():
    cookie_secret = request.cookies.get('cookie_secret')
    auth = request.authorization
    if request.method == 'POST' and str(cookie_secret).__len__() > 1 and auth and auth.username == 'Akwarysta69' and auth.password == 'J3si07r':
        resp = make_response(redirect('/'))
        resp.set_cookie('cookie_secret', '')
        return resp
    return make_response('Could not verify your login', 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})
 
 
@app.route('/fishes', methods=['GET', 'POST'])
@basic_auth.required
def fishes_path():
    cookie_secret = request.cookies.get('cookie_secret')
    auth = request.authorization
    if str(cookie_secret).__len__() > 1 and auth and auth.username == 'Akwarysta69' and auth.password == 'J3si07r':
        if request.method == 'GET':
            return fishes_all()
        elif request.method == 'POST':
            return fishes_add()
    return make_response('Could not verify your login', 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})
 
 
def fishes_all():
    global fishes
    return jsonify(fishes)
 
 
def fishes_add():
    data = request.get_json()
    new_fish = {
        "who": data.get("who"),
        "where": {
            "lat": data['where']['lat'],
            "long": data['where']['long']
        },
        "mass": data.get("mass"),
        "length": data.get("length"),
        "kind": data.get("kind")
    }
 
    global fishes
    fishes[f'id_{fishes.__len__()+1}'] = new_fish
    return "OK"
 
 
@app.route('/fishes/<id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
@basic_auth.required
def fish_one(id):
    cookie_secret = request.cookies.get('cookie_secret')
    auth = request.authorization
    if str(cookie_secret).__len__() > 1 and auth and auth.username == 'Akwarysta69' and auth.password == 'J3si07r':
        idx = id
        if request.method == 'GET':
            global fishes
            fish = fishes[f'id_{idx}']
            return jsonify(fish)
        elif request.method == 'DELETE':
            del fishes[f'id_{idx}']
            return 'OK'
        elif request.method == 'PUT':
            return fish_put(idx)
        elif request.method == 'PATCH':
            data = request.get_json()
            for k in data:
                fishes[f'id_{idx}'][k] = data.get(k)
            return 'OK'
    return make_response('Could not verify your login', 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})
 
 
def fish_put(idx):
    data = request.get_json()
    new_fish = {
        "who": data.get("who"),
        "where": {
            "lat": data['where']['lat'],
            "long": data['where']['long']
        },
        "mass": data.get("mass"),
        "length": data.get("length"),
        "kind": data.get("kind")
    }
 
    global fishes
    fishes[f'id_{idx}'] = new_fish
    return "OK"
 
 
if __name__ == '__main__':
    app.run(debug=True)