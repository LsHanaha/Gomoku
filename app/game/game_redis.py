import pickle
from typing import Union
from uuid import UUID
from aioredis import Redis

from app.game import game_abc


async def convert_to_binary(game: Union[game_abc.RobotGameABC, game_abc.HotSeatGameABC]):
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


async def store_in_redis(game: Union[game_abc.RobotGameABC, game_abc.HotSeatGameABC], redis: Redis):
    binary = await convert_to_binary(game)
    await redis.hset('game', str(game.uuid), binary)
    return True


async def delete_game(game: Union[game_abc.RobotGameABC, game_abc.HotSeatGameABC], redis: Redis):
    await redis.hdel("game", str(game.uuid))
