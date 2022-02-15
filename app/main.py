import redis
import os
from bottle import run, get

# http server
_http_bind_host = os.getenv('HTTP_BIND_HOST', '0.0.0.0')
_http_listen_port = os.getenv('HTTP_LISTEN_PORT', 9090)

# Redis server
_redis_host = os.getenv('REDIS_HOST', 'localhost')
_redis_port = os.getenv('REDIS_PORT', 6379)
_redis_database = os.getenv('REDIS_DATABASE', 0)
_redis = redis.Redis(host=_redis_host, port=_redis_port, db=_redis_database, decode_responses=True)


@get('/')
def index():
  '''
  Welcome message for curious people
  '''
  return 'Another LDAP - Prometheus Metrics'


@get('/metrics')
def metrics():
  '''
  Read the data from Redis and print each value
  '''
  metrics = []
  for key in _redis.scan_iter():
    metrics.append(str(_redis.get(key)))
  return "\n".join(metrics)

run(host=_http_bind_host, port=_http_listen_port)