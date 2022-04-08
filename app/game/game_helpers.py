from typing import List, Optional, Union
import numpy as np

from app.schemas import game_schemas
from app.game import game_abc
import algo_module


_OPPONENT = {1: 2, 2: 1}


async def check_end_of_game(game: Union[game_abc._GameABC], move: game_schemas.Point,
                            check_surrounded=False) \
        -> Optional[Union[game_schemas.StonesInRow, int]]:
    if game.rule_name != 'Karo':
        victory_status = algo_module.is_victory(game.field, game.curr_player, game.rule_status_code)
        if game.score[game.curr_player - 1] >= 5:
            return 1
        return victory_status

    field = game.field
    up_down = [row[move.col] for row in field]
    left_right = field[move.row]
    up_left_down_right = create_diag(field, move.col, move.row)
    down_left_up_right = create_reverse_diag(field, move.col, move.row)

    if check_surrounded:
        func = _helper_result_surrounded
    else:
        func = _helper_result

    up_count = await func(up_down, move.row, game.curr_player)
    left_count = await func(left_right, move.col, game.curr_player)
    up_left_down_right_count = await func(up_left_down_right[0], up_left_down_right[1], game.curr_player)
    down_left_up_right_count = await func(down_left_up_right[0], down_left_up_right[1], game.curr_player)

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


def create_diag(field, start_x, start_y):
    top_half = []
    bottom_half = []

    x, y = start_x, start_y
    while x < 19 and y >= 0:
        top_half.append(field[y][x])
        x += 1
        y -= 1

    x, y = start_x - 1, start_y + 1
    while x >= 0 and y < 19:
        bottom_half.append(field[y][x])
        x -= 1
        y += 1

    return [*bottom_half[::-1], *top_half], len(bottom_half)


def create_reverse_diag(field, start_x, start_y):
    top_half = []
    bottom_half = []

    x, y = start_x, start_y
    while x >= 0 and y >= 0:
        top_half.append(field[y][x])
        x -= 1
        y -= 1

    x, y = start_x + 1, start_y + 1
    while x < 19 and y < 19:
        bottom_half.append(field[y][x])
        x += 1
        y += 1

    return [*top_half[::-1], *bottom_half], len(top_half) - 1


# if __name__ == '__main__':
#     import random
#     field_ = []
#     for _ in range(19):
#         field_.append([random.randint(0, 2) for _ in range(19)])
#     check_end_of_game(field_, game_schemas.Point(row=7, col=9, uuid=None))
