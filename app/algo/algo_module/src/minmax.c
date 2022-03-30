
#include "algo.h"


int direction[8][2] = {
	{1, 0},
	{1, 1},
	{0, 1},
	{-1, 1},
	{-1, 0},
	{-1, -1},
	{0, -1},
	{1, -1},
};

// Первый захват: 800
// Второй захват: 935
// Третий захват: 1300
// Четвертый захват: 1600
// Четвертый захват: 1800
// Пятый захват:  180000
double get_chatch_score(int n) {
	switch (n) {
		case 0:
			return 40;
		case 1:
			return 40;
		case 2:
			return 40;
		case 3:
			return 40;
		case 4:
			return 1700;
		default:
			return 180000;
	}

}


void create_step(g_env* env, move_info* move, int is_player) {
	move->captured_quantity = 0;
	int player_id = (is_player) ? PLAYER : ENEMY;
	int enemy_id = (!is_player) ? PLAYER : ENEMY;
	// TODO: check capture and make it
	// захват достаточно сделать только тут
	assert(env->desk[move->p.x][move->p.y] == EMPTY);
	if (is_player)
		env->desk[move->p.x][move->p.y] = player_id;
	else
		env->desk[move->p.x][move->p.y] = player_id;
	
	if (!(env->rules & ALLOW_CAPTURE)) {
		// printf("Capture blocked\n");
		return;
	}

	for (int i = 0; i < 8; ++i) {
		int x_diff = direction[i][0];
		int y_diff = direction[i][1];
		if (move->p.x + x_diff * 3 >= 0 && move->p.x + x_diff * 3 < env->size &&
				move->p.y + y_diff * 3 >= 0 && move->p.y + y_diff * 3 < env->size) {
			if (env->desk[move->p.x + x_diff * 3][move->p.y + y_diff * 3] == player_id &&
					env->desk[move->p.x + x_diff * 2][move->p.y + y_diff * 2] == enemy_id &&
					env->desk[move->p.x + x_diff * 1][move->p.y + y_diff * 1] == enemy_id) 
			{
				move->captured_points[move->captured_quantity].x = move->p.x + x_diff * 2;
				move->captured_points[move->captured_quantity].y = move->p.y + y_diff * 2;
				move->captured_quantity += 1;
				env->desk[move->p.x + x_diff * 2][move->p.y + y_diff * 2] = EMPTY;
				move->captured_points[move->captured_quantity].x = move->p.x + x_diff * 1;
				move->captured_points[move->captured_quantity].y = move->p.y + y_diff * 1;
				move->captured_quantity += 1;
				env->desk[move->p.x + x_diff * 1][move->p.y + y_diff * 1] = EMPTY;
			}
		}
	}
	if (move->captured_quantity > 0) {
		if (is_player) {
			env->player_capture += 1;
		} else {
			env->enemy_capture += 1;
		}
	}
}

static void reverse_step(g_env* env, move_info* move) {
	env->desk[move->p.x][move->p.y] = EMPTY;
	for (int i = 0; i < move->captured_quantity; ++i) {
		env->desk[move->captured_points[i].x][move->captured_points[i].y] = ENEMY;
	}
}




static double minmax(g_env* env, fframe* frame, int deep, double alpha, double betta, int is_maximizing_player) {
	// printf("Deep: %d\n", deep);
	int is_game_finished = 0;
	double position_score = estimate_position(env, &is_game_finished, is_maximizing_player ? PLAYER : ENEMY);
	if (env->player_capture >= 5) {
		is_game_finished = 1;
		position_score += 120000;
	} else if (env->enemy_capture >= 5) {
		is_game_finished = 1;
		position_score -= 120000;
	} 
	if (is_game_finished) {
		// printf("is_finished: %d, position_score: %lf\n", is_game_finished, position_score);

	}
	if (deep <= 0 || is_game_finished) {
		// TODO: Если финиш - то проверям еще один раз все ходы. Если финиш сохранился дл всех - умножаем estimate на 1000
		// print_desk(env);
		return position_score; //estimate_position(env); // ????????
		// TODO: объединить is_game_finished и estimate_position - ускорит программу в 2 раза

	}
		// return  is_maximizing_player ?  ;
	fill_possibly_steps(env, frame, is_maximizing_player ? PLAYER : ENEMY);
	if (!frame->moves_quantity) {
		return position_score; //estimate_position(env);
	}
	move_info move;
	if (is_maximizing_player) {
		double max_estimate = -1.0 / 0.0;
		for (int i=0; i < frame->moves_quantity; ++i) {
			move.p = frame->possibly_moves[i];
			// if (!is_step_available(env, &move))
			// 	continue;
			create_step(env, &move, is_maximizing_player);
			// print_desk(env);
			double estimate = minmax(env, frame + 1, deep - 1, alpha, betta, !is_maximizing_player);
			if (move.captured_quantity > 0) {
				estimate += get_chatch_score(env->player_capture);
			}
			reverse_step(env, &move);
			alpha = MAX(estimate, alpha);
			max_estimate = MAX(max_estimate, estimate);
			if (betta < alpha) // ? <=
				break;
		}
		return max_estimate;
	} else {
		double min_estimate = 1.0 / 0.0;
		for (int i=0; i < frame->moves_quantity; ++i) {
			move.p = frame->possibly_moves[i];
			// if (!is_step_available(env, &move))
			// 	continue;
			create_step(env, &move, is_maximizing_player);
			// print_desk(env);
			double estimate = minmax(env, frame + 1, deep - 1, alpha, betta, !is_maximizing_player);
			if (move.captured_quantity > 0) {
				estimate -= get_chatch_score(env->enemy_capture);
			}
			reverse_step(env, &move);
			betta = MIN(estimate, betta);
			min_estimate = MIN(min_estimate, estimate);
			if (betta < alpha) // ? <=
				break;
		}
		return min_estimate;
	}
	return 0.0;
}


// Первый уровень minmax
// Вынесен, чтобы можно было удобно отобрать оптимальные ходы
// Заранее маллочим все необходимое
// в frame храним все возможные ходы и оценки ходов
int minmax_start(g_env* env) {
	fframe* steps_frames = create_frames(env);
	// fframe first_frame;
	// printf("Create first frame fo size: %lld\n", env->size);
	if (init_frame(&env->first_frame, env->size))
		return 1;
	// Всегда рассматриваем соседние с поставленными камушками ходы, + 10 случайных позиций
	fill_possibly_steps(env, &env->first_frame, PLAYER);
	
	// print_steps(&env->first_frame);
	// return 1;
	double alpha = -1.0 /0.0;
	double betta = 1.0 /0.0;
	// double max_estimate = -1.0 /0.0;
	move_info move;
	for (int i=0; i < env->first_frame.moves_quantity; ++i) {
		move.p = env->first_frame.possibly_moves[i];
		// if (!is_step_available(env, &move))
		// 	continue;
		create_step(env, &move, true);
		// print_desk(env);
		double estimate = minmax(env, steps_frames + 1, env->deep - 1, alpha, betta, false);
		// printf("HERE \n");
		if (move.captured_quantity > 0) {
				estimate += get_chatch_score(env->player_capture);
				// printf("Print desk\n");
				// print_desk(env);
		}
		// printf("get estimate: %f\n", estimate);
		env->first_frame.estimate[i] = estimate;
		alpha = MAX(estimate, alpha);
		reverse_step(env, &move);
	}
	// print_steps(&env->first_frame);
	return 0;
}

