


#include "algo.h"


unsigned char desk[10][10] = {
	{1, 1, 1, 1, 1, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
	{0, 0, 1, 0, 0, 1, 0, 1, 0, 0},
	{0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};


int main() {
	struct game_env env;
	env.size = 10;
	env.deep = 1;
	env.enemy_capture = 0;
	env.player_capture = 0;
	// env.desk = desk;
	env.desk = (unsigned char**)calloc(env.size + 1, sizeof(unsigned char*));
	for (ssize_t i = 0; i < env.size; i++) {
		env.desk[i] = (unsigned char*)calloc(env.size, sizeof(unsigned char));
		for (ssize_t j = 0; j < env.size; ++j) {
			env.desk[i][j] = desk[i][j];
		}
	}
	// env.desk[4][4] = PLAYER;
	// env.desk[6][6] = PLAYER;
	// env.desk[6][4] = PLAYER;
	// env.desk[4][6] = PLAYER;
	// env.desk[5][5] = ENEMY;
	// env.desk[2][6] = ENEMY;
	// env.desk[0][7] = 2;
	// env.player = 1;
	env.rules = FREE_THREE | ALLOW_CAPTURE;
	// if (!parse_args(&env, args))
	// 	return NULL;
	print_desk(&env);
	minmax_start(&env);



}