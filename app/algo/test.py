from time import sleep
import algo_module
# print(algo_module.c_fib(5))


# print(algo_module.get_moves([[4, 5], [0, 4]], 4, 10))

# SIZE = 10
print("Start")
# def print_arr(arr):
# 	for line in arr:
# 		print(line)
# 	print("-------------------------------------")

arr = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# [10, 18] - victory

def get_move(arr, player):
	deep = 1
	moves = algo_module.get_moves(arr, player, deep)
	# print("get moves for player ", player, "  ", moves)
	# print(sorted(zip(moves[0], moves[1])))
	best_moves = sorted(zip(moves[0], moves[1]), reverse=True)

	print("Moves:")
	for score, position in best_moves:
		print(f" - {score}: {position}")

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


print(get_move(arr, 2))

# for i in range(0, (SIZE) * 2 - 1):
# 	first_y = min(i, SIZE - 1)
# 	first_x = max(0, i - (SIZE - 1))
# 	# arr[first_y][first_x] = 1
# 	print(first_x, first_y)
# 	for j in range(0, SIZE):
# 		if first_y - j <0 or first_x + j >= SIZE:
# 			break
# 		arr[first_y - j][first_x + j] = 1
# 	# for j in range(abs(min(0, SIZE)), SIZE):
# 	# 	arr[i][j] = 1
# 	print_arr(arr)

# # for (int x = env->size - 1; x > -env->size; --x) {
# # 		for (int y = ABS(MIN(0, env->size)); y < env->size; ++y) {
# # 			check(counter, env->desk[y][x] == EMPTY, env->desk[y][x] == for_player)
# # 		}
# # 		new_line(counter);
# # 	}

