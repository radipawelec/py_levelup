from flask import Flask, request, make_response, render_template, redirect, url_for, jsonify


user = {
		'login': 'Akwarysta69',
		'pass': 'J3si07r',
	}


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

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login(): 
	if request.authorization and request.authorization.username == user['login'] and request.authorization.password == user['pass']:
		resp = redirect(url_for('hello'))
		resp.set_cookie('cookie_secret', user['login'])
		return resp
	return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/hello', methods=['GET'])
def hello():
	cookie = request.cookies.get('cookie_secret')
	if cookie == user['login']:
		return	render_template(
			'hello.html', user=cookie)
	else:
<<<<<<< HEAD
		return make_response('Could not verify', 401)
=======
		resp = redirect(url_for('login'))
		return make_response(resp)
>>>>>>> 7767ee7f3e212dcd5e9ebb6cdddb580115be78d1


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	cookie = request.cookies.get('cookie_secret')
	if cookie == user['login']:
		cookie_secret = request.cookies.get('cookie_secret')
		resp = make_response(
				render_template(
					'logout.html', cookie_secret=cookie_secret
				)
			)
		resp.set_cookie('cookie_secret', '', expires=0)
		return resp
	else:
		resp = redirect(url_for('login'))
		return make_response(resp)


@app.route("/fishes", methods=['GET'])
def fishes_info():
	cookie = request.cookies.get('cookie_secret')
	if cookie == user['login']:
		return jsonify(fishes)
	else:
		resp = redirect(url_for('login'))
		return make_response(resp)

@app.route("/fishes/<fish_id>", methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def fish_info(fish_id):
	cookie = request.cookies.get('cookie_secret')
	if cookie == user['login']:
		if request.method == 'GET':
			return get_fish_info(fish_id)
		elif request.method == 'POST':
			return post_fish_info(fish_id)
		elif request.method == 'DELETE': 
			return delete_fish_info(fish_id)
		elif request.method == 'PUT':
			return put_fish_info(fish_id)
		elif request.method == 'PATCH':
			return patch_fish_info(fish_id)
	else:
		resp = redirect(url_for('login'))
		return make_response(resp)

def get_fish_info(fish_id):
    fish = fishes.get(fish_id)
    return jsonify(
    	who=fish.get('who'),
    	where=fish.get('where'),
    	mass=fish.get('mass'),
    	length=fish.get('length'),
    	kind=fish.get('kind'),
    	)

def patch_fish_info(fish_id):
	global fish
	fishid = fish_id
	fish = fishes.get(fish_id)
	data = request.get_json()

	if data.get('who'):
		who = data.get('who')
	else:
		who = fish.get('who')

	if data.get('where'):
		where = data.get('where')
	else:
		where = fish.get('where')

	if data.get('kind'):
		kind = data.get('kind')
	else:
		kind = fish.get('kind')	

	if data.get('length'):
		length = data.get('length')
	else:
		length = fish.get('length')
	
	if data.get('mass'):
		mass = data.get('mass')
	else:
		mass = fish.get('mass')

	new_fish = {
		'who': who,
		'where': where,
		'mass': mass,
		'length': length,
		'kind': kind
	}
	
	fishes[fishid].update(new_fish)
	return 'patched' 

def put_fish_info(fish_id):
	fishid = fish_id
	data = request.get_json()
	new_fish = {
		'who': data.get('who'),
		'where': data.get('where'),
		'mass': data.get('mass'),
		'length': data.get('length'),
		'kind': data.get('kind')
	}
	global fishes
	fishes[fishid] = new_fish 
	return 'putted'


def delete_fish_info(fish_id):
	fishid = fish_id
	global fishes
	fishes.pop(fishid)
	return 'removed'
    

def get_fish_info(fish_id):
    fish = fishes.get(fish_id)
    return jsonify(
    	who=fish.get('who'),
    	where=fish.get('where'),
    	mass=fish.get('mass'),
    	length=fish.get('length'),
    	kind=fish.get('kind'),
    	)

def post_fish_info(fish_id):
	fishid = fish_id
	data = request.get_json()
	new_fish = {
		'who': data.get('who'),
		'where': data.get('where'),
		'mass': data.get('mass'),
		'length': data.get('length'),
		'kind': data.get('kind')
	}
	global fishes
	fishes[fishid] = new_fish 
	return 'added'



if __name__ == '__main__':
	app.run(debug=True)