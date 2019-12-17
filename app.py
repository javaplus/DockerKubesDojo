from arguments import args
from flask import Flask, Response, request, json
import logging
import os
import redis
import time

app = Flask(__name__)

LISTEN_HOST = args.host
LISTEN_PORT = args.port
REDIS_HOST = args.redis_host
REDIS_PORT = args.redis_port

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
livenessDelay = 0

@app.route('/')
def root():
    data = json.dumps({
        "appName": "cloud-native-demo",
        "version": "1.0.0",
        "redis-host": REDIS_HOST,
        "env": {
            "host": os.getenv('HOSTNAME'),
            "user_defined_1": os.getenv('USER_DEFINED_1'),
            "user_defined_2": os.getenv('USER_DEFINED_2'),
            "user_defined_3": os.getenv('USER_DEFINED_3')
        }
    })
    return Response(data, mimetype="application/json")

@app.route('/counter')
def counter():
    hostname = os.getenv("HOSTNAME")

    try:
        if redis_client.hexists("hosts", hostname):
            redis_client.hincrby("hosts", hostname, amount=1)
        else:
            redis_client.hset("hosts", hostname, 1)

        return Response(json.dumps(redis_client.hgetall("hosts")), status=200, mimetype="application/json")
    except:
        return Response(json.dumps({"error": "service unavailable"}), status=503, mimetype="application/json")

@app.route('/counter/reset')
def clear_counter():
    hosts = redis_client.hgetall("hosts")
    [redis_client.hdel("hosts", key) for key in hosts.keys()]
    return Response(json.dumps(redis_client.hgetall("hosts")), status=200, mimetype="application/json")

@app.route('/live')
def live_get():
    time.sleep(livenessDelay)
    return Response(json.dumps({"delay": livenessDelay}), status=200, mimetype="application/json")

@app.route('/live/<int:delay>')
def live_post(delay):
    global livenessDelay
    livenessDelay = delay
    return Response(json.dumps({"delay": livenessDelay}), status=200, mimetype="application/json")

@app.route('/ready')
def ready():
    redis_ready = False

    try:
        redis_ready = redis_client.ping()
    except:
        logging.warning("python connection down")

    response = Response(mimetype="application/json")

    if redis_ready:
        response.status = "200"
        response.response = json.dumps({
            "redis_connection": "up"
        })
    else:
        response.status = "503"
        response.response = json.dumps({
            "redis_connection": "down"
        })

    return response

if __name__ == '__main__':
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
