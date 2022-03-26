from audioop import reverse
import random
from app.game.game_interfaces import RobotGame
import algo_module
from pprint import pprint
import time


from app.schemas import game_schemas



async def _min_max(game: RobotGame) -> game_schemas.Point:
    # col = random.randint(0, 18)
    # row = random.randint(0, 18)
    # TODO place where I added your script
    start_time = time.time() * 1000
    # for line in game.field
    pprint(game.field)
    depth = game.algorithm_depth
    # if sum(sum(game.field, [])) < 8:
    #     print("Start Game")
    #     depth = max(depth, 4)
    moves = algo_module.get_moves(game.field, game.curr_player, depth)
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
    pprint(moves)
    print("select: ", max_move)

    print("---------\n\n")

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

