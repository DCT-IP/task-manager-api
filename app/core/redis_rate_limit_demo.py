from app.core.redis_client import redis_client

def increment_counter(user_id: int):
    key = f"rate:{user_id}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)

    return count