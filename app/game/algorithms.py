from audioop import reverse
import random
from app.game.game_interfaces import RobotGame
import algo_module
from pprint import pprint
import time


from app.schemas import game_schemas


ALLOW_CAPTURE = 0b00001
FREE_THREE = 0b00010
RESTRICTED_SQUARE = 0b00100


async def _min_max(game: RobotGame) -> game_schemas.Point:
    # col = random.randint(0, 18)
    # row = random.randint(0, 18)
    # TODO place where I added your script
    start_time = time.time() * 1000
    # for line in game.field
    rules = 0
    if True:
        rules |= ALLOW_CAPTURE
    # if True:
    #     rules |= FREE_THREE
    if True:
        rules |= RESTRICTED_SQUARE
    pprint(game.field)
    depth = game.algorithm_depth
    # if sum(sum(game.field, [])) < 8:
    #     print("Start Game")
    #     depth = max(depth, 4)
    player_capture = 0
    enemy_capture = 0
    moves = algo_module.get_moves(game.field, game.curr_player, depth, rules, player_capture, enemy_capture)
    game.last_robot_time = time.time() * 1000 - start_time
    debug = []
    print("---------")
    max_estimate = max(moves[0])
    max_index = moves[0].index(max_estimate)
    max_move =  moves[1][max_index]
    best_moves = sorted(zip(moves[0], moves[1]), reverse=True)

    print("Moves:")
    for score, position in best_moves:
        print(f" - {score}: {position}")

    for i in range(min(len(best_moves), 5)):
        debug.append(best_moves[i][1])
    

    # проверяем, что камень можно поставить сюда, согласно правилам:
    # if algo_module.is_step_allowed(game.field, game.curr_player, rules, max_move[0], max_move[1]):
    #     # Ставим камень, если включен захват - убираем лишние камни с поля
    #     other_player = 1 if game.curr_player == 2 else 2
    #     algo_module.implement_move(game.field, game.curr_player, other_player, rules, max_move[0], max_move[1])
    #     PLAYER_WIN = 1
    #     ENEMY_WIN = 2
    #     victory_status = algo_module.is_victory(game.field, game.curr_player, rules)
    #     if victory_status == PLAYER_WIN:
    #         print("Player win")
    #     elif victory_status == ENEMY_WIN:
    #         print("ENEMY win")

    game.debug_data = debug
    return game_schemas.Point(
        row=max_move[0],
        col=max_move[1],
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

