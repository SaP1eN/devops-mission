from flask import Flask
import redis
import socket

app = Flask(__name__)

# Connect to Redis
# Hostname is 'redis-db' because that is what we will name the container in docker-compose
cache = redis.Redis(host='redis-db', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        
        except redis.execptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1

@app.route('/')
def hello():
    count = get_hit_count()
    return f"Hello! I have been seen {count} times. (Host: {socket.gethostname()})"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
