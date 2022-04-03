from typing import Union, Optional
from sqlalchemy.orm import Session
from aioredis import Redis

from app.schemas import game_schemas
from app.game import game_interfaces
from app.game import game_redis
from app.errors import GomokuError


class Arena:

    def __init__(self, db: Session, redis: Redis):
        self._db = db
        self._redis = redis

    async def run(self,
                  game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                  move: game_schemas.Point) -> game_schemas.GameResponse:

        await self._check_rule(game, move)
        await self._set_move(game, move)
        winner_checked = await self._check_rule(game, move, after_move=True)
        if not winner_checked:
            await self._check_end_of_game(game, move)
        if game.has_winner:
            return await self._end_of_game(game)
        await self._change_player(game)
        if end_game_data := await self.run_algorithm(game):
            return end_game_data
        await self._store_game(game)
        return await self._make_response(game)

    async def _check_rule(self,
                          game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                          move: game_schemas.Point,
                          after_move=False) -> None:
        winner_checked = await game.check_rule(game, move, after_move)
        return winner_checked

    @staticmethod
    async def _set_move(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                        move: game_schemas.Point):
        await game.set_move(move)

    async def _check_end_of_game(self, game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame],
                                 move: game_schemas.Point):
        await game.check_end_of_game(move)
        if game.has_winner:
            await game.perform_end_of_game(self._db, self._redis)

    @staticmethod
    async def _change_player(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        await game.change_player()

    @staticmethod
    async def _end_of_game(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]) \
            -> game_schemas.GameResponse:
        end_game = game_schemas.GameEnd(winner=game.curr_player, score=[val * 2 for val in game.score],
                                        count_of_turns=game.count_of_turns)
        return game_schemas.GameResponse(game_end=end_game, game_continue=None)

    async def run_algorithm(self, game: Union[game_interfaces.RobotGame,
                                              game_interfaces.HotSeatGame]) \
            -> Optional[game_schemas.GameResponse]:
        if isinstance(game, game_interfaces.HotSeatGame):
            return
        while True:
            robo_move = await game.run_algorithm(game)
            try:
                await self._check_rule(game, robo_move)
                break
            except GomokuError:
                pass
        await self._set_move(game, robo_move)
        winner_checked = await self._check_rule(game, robo_move, after_move=True)
        if not winner_checked:
            await self._check_end_of_game(game, robo_move)
        if game.has_winner:
            return await self._end_of_game(game)
        await self._change_player(game)

    @staticmethod
    async def _make_response(game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]) \
            -> game_schemas.GameResponse:
        game_continue = await game.make_response()
        return game_schemas.GameResponse(game_continue=game_continue, game_end=None)

    async def _store_game(self, game: Union[game_interfaces.RobotGame, game_interfaces.HotSeatGame]):
        await game_redis.store_in_redis(game, self._redis)
