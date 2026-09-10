# config/settings/test.py
from .settings import *  

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["REDIS_URL"],
        },
    },
}