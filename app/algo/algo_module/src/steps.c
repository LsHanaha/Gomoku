
#include "algo.h"
#include <stdlib.h>


// free-three:
// Можно ли поставить еще один камень так, чтобы получить не закрытую четверку?

// Situation 0 - no free-three
//  [..X**.]	1  // Back Situation 1
//  [O.X**..]	2  // Back Situation 2
//  [O.X.**.]	3  // Back Situation 2
//  [O.X*.*.]	4  // Back Situation 2
//  [.*X.*.]	5  // Back Situation 3
//  [.*X*..]	6  // Back Situation 3

#define SITUATION_0 0
#define SITUATION_1 1
#define SITUATION_2 2
#define SITUATION_3 3
#define SITUATION_4 4
#define SITUATION_5 5
#define SITUATION_6 6


int check_back_line(g_env *env, int x, int y, int x_direction, int y_direction, int player) {
	int point_1 = ENEMY;  // точка на растоянии 1
	int point_2 = ENEMY;  // точка на растоянии 2

	if (x + x_direction >= 0 && x + x_direction < env->size &&
			y + y_direction >= 0 && y + y_direction < env->size) {
		point_1 = env->desk[x + x_direction][y + y_direction];
		if (point_1 == player) {
			point_1 = PLAYER;
		} else if (point_1 != EMPTY) {
			point_1 = ENEMY;
		}
	}
	if (x + x_direction * 2 >= 0 && x + x_direction * 2 < env->size &&
			y + y_direction * 2 >= 0 && y + y_direction * 2 < env->size) {
		point_2 = env->desk[x + x_direction * 2][y + y_direction * 2];
		if (point_2 == player) {
			point_2 = PLAYER;
		} else if (point_2 != EMPTY) {
			point_2 = ENEMY;
		}
	}
	if (point_1 == EMPTY && point_2 == EMPTY) {
		return SITUATION_1;
	} else if (point_1 == EMPTY) {
		return SITUATION_2;
	} else if (point_1 == PLAYER && point_2 == EMPTY) {
		return SITUATION_3;
	}
	return SITUATION_0;
}

// Situation 0 - no free-three
//  [..X**.]	1  // Front Situation 1
//  [O.X**..]	2  // Front Situation 2 and 1 
//  [O.X.**.]	3  // Front Situation 3
//  [O.X*.*.]	4  // Front Situation 4
//  [.*X.*.]	5  // Front Situation 5
//  [.*X*..]	6  // Front Situation 6

static int check_front_line(g_env *env, int x, int y, int x_direction, int y_direction, int player) {
	int points[4] = {ENEMY, ENEMY, ENEMY, ENEMY};  // точки на растоянии до 4

	for (int i = 0; i < 4; ++i ) {
		int check_x = x + x_direction * (i + 1);
		int check_y = y + y_direction * (i + 1);
		if (check_x >= 0 && check_x < env->size &&
				check_y >= 0 && check_y < env->size) {
			points[i] = env->desk[check_x][check_y];
			if (points[i] == player) {
				points[i] = PLAYER;
			}  else if (points[i] != EMPTY) {
				points[i] = ENEMY;
			}
		}

	}
	if (points[0] == ENEMY) {
		return SITUATION_0;
	}
	if (points[0] == PLAYER && points[1] == PLAYER && points[2] == EMPTY && points[3] == EMPTY) {
		return SITUATION_2;
	} else if (points[0] == PLAYER && points[1] == PLAYER && points[2] == EMPTY) {
		return SITUATION_1;
	} else if (points[0] == EMPTY && points[1] == PLAYER && points[2] == PLAYER && points[3] == EMPTY) {
		return SITUATION_3;
	} else if (points[0] == PLAYER && points[1] == EMPTY && points[2] == PLAYER && points[3] == EMPTY) {
		return SITUATION_4;
	} else if (points[0] == EMPTY && points[1] == PLAYER && points[2] == EMPTY) {
		return SITUATION_5;
	} else if (points[0] == PLAYER && points[1] == EMPTY && points[2] == EMPTY) {
		return SITUATION_6;
	}
	return SITUATION_0;
}

// [BACK.X.FRONT]
// Situation 0 - no free-three
//  [..X**.O]	1  // Back Situation 1
//  [O.X**..]	2  // Back Situation 2
//  [O.X.**.]	3  // Back Situation 2
//  [O.X*.*.]	4  // Back Situation 2
//  [.*X.*.]	5  // Back Situation 3
//  [.*X*..]	6  // Back Situation 3

//  [..X**.O]	1  // Front Situation 1 and 2  - Back Situation 1
//  [O.X**..]	2  // Front Situation 2		   - Back Situation 2 or 1
//  [O.X.**.]	3  // Front Situation 3		   - Back Situation 2 or 1
//  [O.X*.*.]	4  // Front Situation 4		   - Back Situation 2 or 1
//  [.*X.*.]	5  // Front Situation 5		   - Back Situation 3
//  [.*X*..]	6  // Front Situation 6		   - Back Situation 3

static int check_free_three(g_env *env, int x, int y, int x_direction, int y_direction, int player) {
	int front_situation = check_front_line(env, x, y, x_direction, y_direction, player);
	int back_situation = check_back_line(env, x, y, -x_direction, -y_direction, player);

	if (front_situation == SITUATION_0 || back_situation == SITUATION_0) {
		return false;
	} else if (back_situation == SITUATION_1 && (front_situation == SITUATION_1 || front_situation == SITUATION_2)) {
		return true;
	} else if ((back_situation == SITUATION_2 || back_situation == SITUATION_1) && (front_situation == SITUATION_2 || front_situation == SITUATION_3 ||
																					front_situation == SITUATION_4)) {
		return true;
	} else if (back_situation == SITUATION_3 && (front_situation == SITUATION_5 || front_situation == SITUATION_6)) {
		return true;
	}
	return false;
}



int is_step_allowed(g_env *env, int x, int y, int player) {
	if (env->rules & FREE_THREE) {
		int free_three_counter = 0;
		for (int i = 0; i < 4; ++i) {
			// каждый раз смотрим в обе стороны, поэтому достаточно проверить 4 направления
			int x_direction = direction[i][0];
			int y_direction = direction[i][1];

			int is_free_three = check_free_three(env, x, y, x_direction, y_direction, player) || 
								check_free_three(env, x, y, -x_direction, -y_direction, player);
			if (is_free_three) {
				// printf("Find Free-Three! step x: %d, y: %d\n", x, y);
				++free_three_counter;
			}
		}
		if (free_three_counter > 1) {
			// printf("Block by  Free-Three rule. step x: %d, y: %d\n", x, y);
			return false;
		}
	}

	return true;
}

static void add_random_steps(g_env* env, fframe* frame, int attempt, int player) {
	for (int i = 0; i < attempt; ++i) {
		if (frame->moves_quantity > env->size * env->size)
			break;
		int x = rand() % env->size;
		int y = rand() % env->size;
		// printf("Try random step: %d %d\n", x, y);
		if (env->desk[x][y] == EMPTY && is_step_allowed(env, x, y, player)) {
			frame->possibly_moves[frame->moves_quantity].x = x;
			frame->possibly_moves[frame->moves_quantity].y = y;
			++(frame->moves_quantity);
		}
	}
}

double estimate_step(g_env* env, ppoint* point, int player) {
	double score = 0.0;
	int x = point->x;
	int y = point->y;

	for (int i = 0; i < 8; ++i) {
		double line = 0.0;
		int x_direction = direction[i][0];
		int y_direction = direction[i][1];
		while (true) {
			x += x_direction;
			y += y_direction;
			if (x >= 0 && x < env->size && y >= 0 && y < env->size &&
												env->desk[x][y] == player)
			{
				++line;
				line = line * 2;
			} else {
				break;
			}

		}
		score += line;
	}
	return score;
}

int compare_steps(const void *p_1, const void *p_2) {
	const ppoint* p1 = (const ppoint*)p_1;
	const ppoint* p2 = (const ppoint*)p_2;
	if (p1->score < p2->score)
        return 1;  // Return -1 if you want ascending, 1 if you want descending order. 
    else if (p1->score > p2->score)
        return -1;   // Return 1 if you want ascending, -1 if you want descending order.
    return 0;
}

void sort_steps(g_env* env, fframe* frame, int player) {
	for (int i = 0; i < frame->moves_quantity; ++i) {
		frame->possibly_moves[i].score = estimate_step(env, &frame->possibly_moves[i], player);
	}
	qsort(frame->possibly_moves, frame->moves_quantity, sizeof(ppoint), compare_steps);
}

void fill_possibly_steps(g_env* env, fframe* frame, int player) {
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
			if (has_neighbor && is_step_allowed(env, i, j, player)) {
				frame->possibly_moves[current_step].x = i;
				frame->possibly_moves[current_step].y = j;
				++current_step;
			}
		}
	}
	frame->moves_quantity = current_step;
	sort_steps(env, frame, player);
	add_random_steps(env, frame, RANDOM_STEPS_TRYES, player);
}

void print_steps(fframe* frame) {
	for (ssize_t i = 0; i < frame->moves_quantity; ++i) {
		printf("Find step: %d %d, ", frame->possibly_moves[i].x, frame->possibly_moves[i].y);
		printf("Estimate: %f\n", frame->estimate[i]);
	}
}