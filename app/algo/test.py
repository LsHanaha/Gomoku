
from time import sleep
import algo_module
# print(algo_module.c_fib(5))

from pprint import pprint
# print(algo_module.get_moves([[4, 5], [0, 4]], 4, 10))

# SIZE = 10
print("Start")
# def print_arr(arr):
# 	for line in arr:
# 		print(line)
# 	print("-------------------------------------")

arr = [
 [2, 2, 2, 0, 2, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# [10, 18] - victory

ALLOW_CAPTURE = 0b00001
FREE_THREE = 0b00010
RESTRICTED_SQUARE = 0b00100

def get_move(arr, player):
    deep = 1
    rules = 0
    if True:
        rules |= ALLOW_CAPTURE
    if True:
        rules |= FREE_THREE
    if True:
        rules |= RESTRICTED_SQUARE
    # if sum(sum(game.field, [])) < 8:
    #     print("Start Game")
    #     depth = max(depth, 4)
    player_capture = 0
    enemy_capture = 0
    moves = algo_module.get_moves(arr, player, deep, rules, player_capture, enemy_capture)
    # print("get moves for player ", player, "  ", moves)
    # print(sorted(zip(moves[0], moves[1])))
    best_moves = sorted(zip(moves[0], moves[1]), reverse=True)

    print("Moves:")
    for score, position in best_moves:
        print(f" - {score}: {position}")
        break

    max_estimate = max(moves[0])
    max_index = moves[0].index(max_estimate)
    print(moves[1][max_index])
    return moves[1][max_index]

# for i in range(20):
# 	move = get_move(arr, 1)
# 	arr[move[0]][move[1]] = 1
# 	print_arr(arr)
# 	# sleep(1)
# 	move = get_move(arr, 2)
# 	arr[move[0]][move[1]] = 2
# 	print_arr(arr)
# 	# sleep(1)

def test_1():
    print(get_move(arr, 2))

# test_1()



def test_2():
    deep = 1
    rules = 0
    # if True:
    #     rules |= ALLOW_CAPTURE
    if True:
        rules |= FREE_THREE
    if True:
        rules |= RESTRICTED_SQUARE
    # if sum(sum(game.field, [])) < 8:
    #     print("Start Game")
    #     depth = max(depth, 4)
    player_capture = 0
    enemy_capture = 0
    player = 2
    enemy = 1
    x = 0
    y = 9
    moves = algo_module.implement_move(arr, player, enemy, rules, x, y)
    pprint(moves)

# test_2()

EMPTY = 0
PLAYER = 1
ENEMY = 2
def test_3():
    deep = 1
    rules = 0
    # if True:
    #     rules |= ALLOW_CAPTURE
    if True:
        rules |= FREE_THREE
    if True:
        rules |= RESTRICTED_SQUARE
    # if sum(sum(game.field, [])) < 8:
    #     print("Start Game")
    #     depth = max(depth, 4)
    player_capture = 0
    enemy_capture = 0
    player = 2
    # # enemy = 2
    # x = 0
    # y = 9
    victory = algo_module.is_victory(arr, player, rules)
    if victory == EMPTY:
        print("No victory")
    if victory == PLAYER:
        print("Player victory")
    if victory == ENEMY:
        print("Enemy victored")

    # pprint(moves)


test_3()

