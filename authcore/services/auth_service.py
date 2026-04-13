import os
import redis
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

redis_client= redis.Redis(host="redis", port=6379,db=0, decode_responses=True)

def generate_jwt(user):
    refresh_ttl = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    access_ttl = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())

    refresh = RefreshToken.for_user(user)
    refresh_token = str(refresh)
    access_token = str(refresh.access_token)
    redis_client.setex(access_token, access_ttl, refresh_token)
    redis_client.setex(refresh_token, refresh_ttl, str(user.id))

    return {
    "access_token": access_token,
    "refresh_token": refresh_token
    }



def invalidate_jwt(access_token: str):
    refresh_token = redis_client.get(access_token)

    # 2. If session exists, delete both
    if refresh_token:
        redis_client.delete(access_token)
        redis_client.delete(refresh_token)

    