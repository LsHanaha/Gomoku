from aioredis import Redis
from uuid import UUID
from typing import Union, Optional
from sqlalchemy.orm import Session

from app.errors import GomokuError
from app.schemas import game_schemas
from app.game.game_interfaces import RobotGame, HotSeatGame
from app.game.game_redis import load_from_redis
from app.crud.game import get_queries


async def init_game_data(redis: Redis, uuid: UUID) -> Optional[game_schemas.InitGameData]:
    game: Union[RobotGame, HotSeatGame] = await load_from_redis(uuid, redis)
    if not game:
        return None
    game_data = game_schemas.InitGameData(
        game_mode="hotseat" if isinstance(game, HotSeatGame) else "robot",
        field_name=game.field_type,
        dices=game.dice_colors.split(":"),
        current_player=game.curr_player,
        score=game.score,
        count_of_turns=game.count_of_turns,
        rule=game.rule_name,
        debug=False,
        field=game.field
    )
    if isinstance(game, RobotGame):
        game_data.debug = game.is_debug
    return game_data


async def get_user_history(user_id: int, db: Session):
    data = get_queries.get_user_history(user_id, db)
    return data
