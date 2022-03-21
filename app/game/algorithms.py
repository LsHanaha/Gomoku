import random
from uuid import UUID
from app.game.game_interfaces import RobotGame

from app.schemas import game_schemas


async def _min_max(game: RobotGame) -> game_schemas.Point:
    col = random.randint(0, 18)
    row = random.randint(0, 18)
    game.last_robot_time = random.randint(100, 1000)
    game.debug_data = None
    return game_schemas.Point(
        row=row,
        col=col,
        uuid=game.uuid
    )


async def _another(game: RobotGame) -> game_schemas.Point:
    col = random.randint(0, 19)
    row = random.randint(0, 19)
    game.last_robot_time = random.randint(100, 1000)
    game.debug_data = None
    return game_schemas.Point(
        row=row,
        col=col,
        uuid=game.uuid
    )


algorithms = {
    'min-max': _min_max,
    'tosi-bosi': _another
}

