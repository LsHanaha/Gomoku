


#include "algo.h"



int main() {
	struct game_env env;
	env.size = 10;
	env.deep = 2;
	env.enemy_capture = 0;
	env.player_capture = 0;
	env.desk = (unsigned char**)calloc(env.size + 1, sizeof(unsigned char*));
	for (ssize_t i = 0; i < env.size; i++) {
		env.desk[i] = (unsigned char*)calloc(env.size, sizeof(unsigned char));
	}
	env.desk[4][6] = 1;
	env.desk[5][6] = 1;
	env.desk[7][6] = 1;
	env.desk[5][4] = 2;
	env.player = 1;
	// if (!parse_args(&env, args))
	// 	return NULL;
	print_desk(&env);
	minmax_start(&env);



}