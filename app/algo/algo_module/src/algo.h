
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
#define RANDOM_STEPS_TRYES 10
#define WIN_LENGTH 5
#define WIN_ESTIMATE 10000
// #define MAX_DEEP 200

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
	fframe first_frame;
} g_env;





typedef struct s_move_info {
	ppoint p;
	int is_capture;
	ppoint capture_1;
	ppoint capture_2;
} move_info;

// output 
void print_steps(fframe* frame);
void print_desk(struct game_env* env);

int init_frame(fframe* frame, int size);

void free_desk(unsigned char **desk);
int minmax_start(g_env* env);

//estimate
int is_game_finished(g_env* env, int is_maximizing_player);
double estimate_position(g_env* env);

//minmax_init
fframe* create_frames(struct game_env* env);
void free_frames(fframe* steps_frames);

//steps
void fill_possibly_steps(g_env* env, fframe* frame);

#endif