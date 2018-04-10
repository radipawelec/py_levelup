form flask import Flask, request, make_resposne

app = Flask(__name__)

@app.route('/')
def index(): 
	if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'passowrd':
		return '<h1>You are logged in</h1>'

	make_resposne('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})



if __name__ == '__main__':
	app.run(debug=True)