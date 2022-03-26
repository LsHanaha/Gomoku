import random
from app.game.game_interfaces import RobotGame
import algo_module

from app.schemas import game_schemas


async def _min_max(game: RobotGame) -> game_schemas.Point:
    # col = random.randint(0, 18)
    # row = random.randint(0, 18)
    # TODO place where I added your script
    move = algo_module.get_moves(game.field, game.curr_player, game.algorithm_depth)
    game.last_robot_time = random.randint(100, 1000)
    game.debug_data = None
    # game.debug_data = [[0, 0],[1, 1],[2, 2],[3, 3],[4, 4]]
    return game_schemas.Point(
        row=move[0],
        col=move[1],
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

