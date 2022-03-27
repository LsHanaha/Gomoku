
#ifndef ALGO_H
#define ALGO_H

#define PY_SSIZE_T_CLEAN
// The actual Python API
#include <Python.h>



#include <stdio.h>
#include <stdlib.h>
// #define ssize_t long long



#include <assert.h>

#define MAX(x,y) (((x) >= (y)) ? (x) : (y))
#define MIN(x,y) (((x) <= (y)) ? (x) : (y))
#define ABS(x) (((x) <= (0)) ? (-x) : (x))

#define EMPTY 0
#define PLAYER 1
#define ENEMY 2

#define false 0
#define true 1
#define MAX_CAPTURES 5
#define RANDOM_STEPS_TRYES 1
#define WIN_LENGTH 5
#define WIN_ESTIMATE 10000
// #define MAX_DEEP 200

#define ALLOW_CAPTURE 0x00001
#define FREE_THREE 0x00010
#define RESTRICTED_SQUARE 0x00100

extern int direction[8][2];

typedef struct point {
	unsigned char x;
	unsigned char y;
} ppoint;


typedef struct frame {
	ppoint* possibly_moves;
	ssize_t moves_quantity;
	double* estimate;
} fframe;

typedef struct game_env {
	unsigned char **desk;
	ssize_t size;
	unsigned char player;
	unsigned int deep;
	int player_capture;
	int enemy_capture;
	int rules;
	fframe first_frame;
} g_env;





typedef struct s_move_info {
	ppoint p;
	int captured_quantity;
	ppoint captured_points[16];
} move_info;

// output 
void print_steps(fframe* frame);
void print_desk(struct game_env* env);

int init_frame(fframe* frame, size_t size);

void free_desk(unsigned char **desk);
int minmax_start(g_env* env);

void create_step(g_env* env, move_info* move, int is_player);

//estimate
// int is_game_finished(g_env* env, int is_maximizing_player);
double estimate_position(g_env* env, int* is_game_finished, int player);

//minmax_init
fframe* create_frames(struct game_env* env);
void free_frames(fframe* steps_frames);

//steps
void fill_possibly_steps(g_env* env, fframe* frame, int player);

#endif
