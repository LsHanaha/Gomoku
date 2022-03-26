
#include "algo.h"




static void create_step(g_env* env, move_info* move, int is_player) {
	move->is_capture = false;
	// TODO: check capture and make it
	// захват достаточно сделать только тут
	assert(env->desk[move->p.x][move->p.y] == EMPTY);
	if (is_player)
		env->desk[move->p.x][move->p.y] = PLAYER;
	else
		env->desk[move->p.x][move->p.y] = ENEMY;
}

static void reverse_step(g_env* env, move_info* move) {
	env->desk[move->p.x][move->p.y] = EMPTY;
	// if (move->is_capture) {
		// env->desk[move->capture_1.x][move->capture_1.y] = ENEMY;
		// env->desk[move->capture_2.x][move->capture_2.y] = ENEMY;
	// }
}




static double minmax(g_env* env, fframe* frame, int deep, double alpha, double betta, int is_maximizing_player) {
	int is_game_finished = 0;
	double position_score = estimate_position(env, &is_game_finished, is_maximizing_player ? PLAYER : ENEMY);
	if (deep <= 0 || is_game_finished) {
		// print_desk(env);
		return position_score; //estimate_position(env); // ????????
		// TODO: объединить is_game_finished и estimate_position - ускорит программу в 2 раза

	}
		// return  is_maximizing_player ?  ;
	fill_possibly_steps(env, frame);
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
			// steps_frames[0].estimate[i] = estimate;
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
			// steps_frames[0].estimate[i] = estimate;
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
	fill_possibly_steps(env, &env->first_frame);
	
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
		// printf("get estimate: %f\n", estimate);
		env->first_frame.estimate[i] = estimate;
		alpha = MAX(estimate, alpha);
		reverse_step(env, &move);
	}
	// print_steps(&env->first_frame);
	return 0;
}

