from redis import Redis
from app.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    socket_timeout=None
)

redis_windows = Redis(
    host='localhost',
    port=settings.REDIS_PORT,
    decode_responses=True,
    socket_timeout=None
)