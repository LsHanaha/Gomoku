from pydantic import BaseSettings
from functools import lru_cache


class _Settings(BaseSettings):

    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_database: str = "gomoku"
    postgres_database_testing: str = "gomoku_testing"

    secret: str = "95674191eacefbc03ba0db0a90b422163a1cf3f82e9748ce"
    algorithm: str = "HS256"
    token_lifetime_sec: int = 60000
    denylist: bool = True

    mail_token_lifetime: int = 259200
    mail_user: str
    mail_address: str
    mail_pwd: str

    redis_host: str = "localhost"
    redis_port: str = "6379"
    redis_password: str = "iHbYUGy86g67Fyf6767f"
    debug: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return _Settings()


settings = get_settings()
