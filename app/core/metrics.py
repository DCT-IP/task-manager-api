from app.core.redis_client import redis_client

def increment_counter(user_id: int):
    key = f"user:{user_id}:requests"

    count = redis_client.incr(key)

    redis_client.expire(
        key,
        60
    )

    return count