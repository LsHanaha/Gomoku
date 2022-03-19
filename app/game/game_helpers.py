from typing import List, Optional, Union
import numpy as np

from app.schemas import game_schemas
from app.game import game_abc


_OPPONENT = {1: 2, 2: 1}


async def check_end_of_game(game: Union[game_abc._GameABC], move: game_schemas.Point,
                            check_surrounded=False) \
        -> Optional[game_schemas.StonesInRow]:

    field = game.field
    up_down = [row[move.row] for row in field]
    left_right = field[move.row]
    up_left_down_right = np.diagonal(field, offset=(move.col - move.row))
    down_left_up_right = np.diagonal(np.rot90(field), offset=(move.row - (game.field_size - 1 - move.col)))

    if check_surrounded:
        func = _helper_result_surrounded
    else:
        func = _helper_result

    up_count = await func(up_down, move.row, game.curr_player)
    left_count = await func(left_right, move.col, game.curr_player)
    up_left_down_right_count = 1
    down_left_up_right_count = 1

    return game_schemas.StonesInRow(lengths=[up_count, left_count,
                                             up_left_down_right_count, down_left_up_right_count])


async def _helper_result(array: Union[List[int], np.array], start: int, user: int) -> int:
    array[start] = user
    count = 0
    for i in array[start:]:
        if i != user:
            break
        count += 1
    for i in array[:start][::-1]:
        if i != user:
            break
        count += 1
    return count


async def _helper_result_surrounded(array: Union[List[int], np.array], start: int, user: int):
    array[start] = user
    another_user = _OPPONENT[user]
    size = len(array)
    count = 0
    surrounded = True
    i = start
    while i < size:
        if array[i] != user:
            break
        count += 1
        i += 1
    if i < size and array[i] == another_user:
        pass
    else:
        surrounded = False
    i = start - 1
    while i >= 0:
        if array[i] != user:
            break
        count += 1
        i -= 1
    if i >= 0 and array[i] == another_user:
        pass
    else:
        surrounded = False
    return count, surrounded


# if __name__ == '__main__':
#     import random
#     field_ = []
#     for _ in range(19):
#         field_.append([random.randint(0, 2) for _ in range(19)])
#     check_end_of_game(field_, game_schemas.Point(row=7, col=9, uuid=None))
