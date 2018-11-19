import flask
import redis
import time
import json
from flask import Flask
from flask import request
from flask import Response, stream_with_context


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
r  = redis.Redis(host='redis', port=6379)
db  = redis.Redis(host='redis', port=6379)

ttl = 31104000 #one year
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
def set_get():
    
    r.set('foo','bar')
    return  r.get('foo').decode('utf-8')

@app.route('/', defaults={'path': ''}, methods = ['PUT', 'GET'])
@app.route('/<path:path>', methods = ['PUT', 'GET'])
def home(path):
    return'hello'

@app.route('/count')
def hello():
    count = get_hit_count()
    return 'Hello from Docker2! I have been seen {} times.\n'.format(count)



@app.route('/value')
def valueget():
    setget = set_get()
    return 'Value {} \n'.format(setget)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)