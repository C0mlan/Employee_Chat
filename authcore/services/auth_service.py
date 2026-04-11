import os
import redis
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

redis_client= redis.Redis(host="redis", port=6379,db=0, decode_responses=True)

def generate_jwt(user):
    ttl = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())

    token = str(RefreshToken.for_user(user).access_token)
    redis_client.setex(token, ttl, str(user.id))
    return token