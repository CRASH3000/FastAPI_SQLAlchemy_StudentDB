import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value, expire: int = 300):
    redis_client.setex(key, expire, json.dumps(value))