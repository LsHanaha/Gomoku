
#include "algo.h"

static void add_random_steps(g_env* env, fframe* frame, int attempt) {
	for (int i = 0; i < attempt; ++i) {
		if (frame->moves_quantity > env->size * env->size)
			break;
		int x = rand() % env->size;
		int y = rand() % env->size;
		// printf("Try random step: %d %d\n", x, y);
		if (env->desk[x][y] == EMPTY) {
			frame->possibly_moves[frame->moves_quantity].x = x;
			frame->possibly_moves[frame->moves_quantity].y = y;
			++(frame->moves_quantity);
		}
	}
}

void fill_possibly_steps(g_env* env, fframe* frame) {
	size_t current_step = 0;
	for (ssize_t i = 0; i < env->size; ++i) {
		for (ssize_t j = 0; j < env->size; ++j) {
			if (env->desk[i][j] != EMPTY)
				continue;
			int has_neighbor = false;
			for (int x = -1; x < 2; ++x) {
				for (int y = -1; y < 2; ++y) {
					if (i + x >= 0 && i + x < env->size && j + y >= 0 && j + y < env->size) {
						if (env->desk[i + x][j + y] != EMPTY) {
							has_neighbor = true;
							break;
						}
					}
				}
				if (has_neighbor)
					break;
			}
			if (has_neighbor) {
				frame->possibly_moves[current_step].x = i;
				frame->possibly_moves[current_step].y = j;
				++current_step;
			}
		}
	}
	frame->moves_quantity = current_step;
	add_random_steps(env, frame, RANDOM_STEPS_TRYES);
}

void print_steps(fframe* frame) {
	for (ssize_t i = 0; i < frame->moves_quantity; ++i) {
		printf("Find step: %d %d, ", frame->possibly_moves[i].x, frame->possibly_moves[i].y);
		printf("Estimate: %f\n", frame->estimate[i]);
	}
}