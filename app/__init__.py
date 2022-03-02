from aioredis import from_url
from typing import AsyncIterator

from redis import Redis
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from app.config import settings


async def get_async_redis_conn() -> AsyncIterator[Redis]:
    try:
        conn = await from_url(f"redis://:{settings.redis_password}@"
                              f"{settings.redis_host}:{settings.redis_port}")
        return conn
    except ConnectionRefusedError as e:
        raise Exception(e)


sync_redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0,
                   decode_responses=True, encoding='utf-8', password=settings.redis_password)


# настройка jwt-auth, все подхватывается приложением
class Settings(BaseModel):
    authjwt_secret_key: str = settings.secret
    authjwt_denylist_enabled: bool = bool(settings.denylist)
    authjwt_denylist_token_checks: set = {"access", "refresh"}


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token.get('jti')
    if not jti:
        return True
    in_denylist = sync_redis.hget('token', jti)
    return in_denylist == 'true'
