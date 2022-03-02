from typing import Union
from sqlalchemy.orm import Session
from aioredis import Redis

from app.schemas import game_schemas
from app.game import game_interfaces
from app.game import game_in_redis
from app.errors import GomokuError


class _Arena:

    def __init__(self, db: Session, redis: Redis):
        self._db = db
        self._redis = redis

    async def run(self,
                  game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                  move: game_schemas.Point):

        # clear response field in the game
        game.to_response = None

        await self._check_rule()
        await self._set_move(game, move)
        await self._check_end_of_game(game)
        has_winner = await self._end_of_game(game)
        if has_winner:
            return
        await self.run_algorithm()
        await self._make_response()
        await self._store_game(game)

    async def _check_rule(self):
        pass

    @staticmethod
    async def _set_move(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                        move: game_schemas.Point):
        await game.set_move(move)

    async def _check_end_of_game(self, game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        await game.check_end_of_game()
        if game.has_winner:
            await game.perform_end_of_game(self._db)

    @staticmethod
    async def _change_player(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        await game.change_player()

    @staticmethod
    async def _end_of_game(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        if game.has_winner:
            return True

    async def run_algorithm(self):
        pass

    async def _make_response(self):
        pass

    async def _store_game(self, game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        await game_in_redis.store_in_redis(game, self._redis)
