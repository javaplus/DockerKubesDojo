import argparse

parser = argparse.ArgumentParser(description='Starter Python + Redis app')
parser.add_argument('--port', '-p', type=int, required=False, help="port number to listen for HTTP requests", default=5000)
parser.add_argument('--host', type=str, required=False, help="host to bind to", default='0.0.0.0')
parser.add_argument('--redis-host', type=str, required=False, help="hostname of the backing Redis service", default='localhost')
parser.add_argument('--redis-port', type=str, required=False, help="port number of the backing Redis service", default='6379')

args = parser.parse_args()
