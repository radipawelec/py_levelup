from flask import Flask, request
from datetime import datetime



app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/now')
def now():
    return f'{datetime.utcnow()}'


@app.route('/request')
def request_info():
    return f'request method: {request.method} url: {request.url} headers: {request.headers}'

    
@app.route('/user-agent')
def userAgent_info():
    dv = request.user_agent.platform
    if dv == "windows" or dv == "macos" or dv == "linux":
        dv2 = "PC"
    else:
        dv2 = "Mobile"
    return f' {dv2} / {request.user_agent.platform.title()} / {request.user_agent.browser.title()} {request.user_agent.version.title()}'

@app.route('/counter')
def counter():
    plik = open('cnt').read()
    i = int(plik)
    j = i + 1
    plik = open('cnt', 'w').write(str(j))
    return str(j)

if __name__ == '__main__':
    app.run(debug=True)