import random
from common.redis import redis_client


CODE_TTL = 300  


def generate_code() -> str:
    return str(random.randint(100000, 999999))


def save_confirmation_code(email: str, code: str) -> None:
    key = f"confirmation_code:{email}"
    redis_client.setex(key, CODE_TTL, code)


def get_confirmation_code(email: str) -> str | None:
    key = f"confirmation_code:{email}"
    return redis_client.get(key)


def delete_confirmation_code(email: str) -> None:
    key = f"confirmation_code:{email}"
    redis_client.delete(key)
