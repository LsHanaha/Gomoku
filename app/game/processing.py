from aioredis import Redis
from uuid import UUID
from typing import Union

from app.errors import GomokuError
from app.schemas import game_schemas
from app.game.game_interfaces import RobotGame, HotSeatGame
from app.game.game_redis import load_from_redis


async def init_game_data(redis: Redis, uuid: UUID) -> game_schemas.InitGameData:
    game: Union[RobotGame, HotSeatGame] = await load_from_redis(uuid, redis)
    game_data = game_schemas.InitGameData(
        game_mode="hotseat" if isinstance(game, HotSeatGame) else "robot",
        field=game.field_type,
        dices=game.dice_colors.split(":"),
        current_player=game.curr_player,
        score=game.score,
        count_of_turns=game.count_of_turns,
        rule=game.rule_name,
        debug=False
    )
    if isinstance(game, RobotGame):
        game_data.debug = game.is_debug
    return game_data
