import random
import algo_module
import time


from app.game.game_interfaces import RobotGame
from app.schemas import game_schemas


async def _min_max(game: RobotGame, depth_force=0) -> game_schemas.Point:
    try:
        depth = game.algorithm_depth if game.algorithm_depth else depth_force
    except AttributeError:
        depth = depth_force
    curr_player = game.curr_player
    start_time = time.time() * 1000
    moves = algo_module.get_moves(game.field, game.curr_player,
                                  depth, game.rule_status_code,
                                  game.score[0 if curr_player == 1 else 1],
                                  game.score[1 if curr_player == 1 else 0])
    debug = []

    max_estimate = max(moves[0])
    max_index = moves[0].index(max_estimate)
    max_move = moves[1][max_index]
    best_moves = sorted(zip(moves[0], moves[1]), reverse=True)
    game.last_robot_time = time.time() * 1000 - start_time

    if getattr(game, 'is_debug', None):
        for i in range(min(len(best_moves), 5)):
            debug.append(best_moves[i][1])
    game.debug_data = debug


    # проверяем, что камень можно поставить сюда, согласно правилам:
    #  max_move[0], max_move[1] - x, y на карте, координаты которые нам интересны
    # if algo_module.is_step_allowed(game.field, game.curr_player, rules, max_move[0], max_move[1]):
    #     # Ставим камень, если включен захват - убираем лишние камни с поля
    #     other_player = 1 if game.curr_player == 2 else 2
    #     модифицирует поле для случая взятий
    #     algo_module.implement_move(game.field, game.curr_player, other_player, rules, max_move[0], max_move[1])
    #     victory_status = algo_module.is_victory(game.field, game.curr_player, rules)

    return game_schemas.Point(
        row=max_move[0],
        col=max_move[1],
        uuid=game.uuid
    )


async def _random(game: RobotGame) -> game_schemas.Point:
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
    'random': _random
}

