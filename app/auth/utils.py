from app import sync_redis


def add_token_to_revoke_list(token_jti):
    sync_redis.hset('token', token_jti, 'true')
