import pickle
from typing import Union
from uuid import UUID
from aioredis import Redis

from app.game.game_interfaces import RobotGame, HotSeatGame


async def convert_to_binary(game: Union[RobotGame, HotSeatGame]):
    binary = pickle.dumps(game)
    return binary


async def convert_from_binary(binary: bytes):
    game = pickle.loads(binary)
    return game


async def load_from_redis(uuid: UUID, redis: Redis):
    binary = await redis.hget('game', str(uuid))
    if binary is None:
        return None
    game = await convert_from_binary(binary)
    return game


async def store_in_redis(game: Union[RobotGame, HotSeatGame], redis: Redis):
    binary = await convert_to_binary(game)
    await redis.hset('game', str(game.uuid), binary)
    return True
